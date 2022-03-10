# import time
from random import choice

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask_mysqldb import MySQL
from flask_session import Session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from ai import minimax
from config import Config
from forms import LoginForm, RegistrationForm
from game import Game, Game_AI

# creates the Flask instance. Passes the argument __name__ which is the name of the application's module. It needs to know this in order for flask to know where to look for resourses.
app = Flask(__name__)

app.config.from_object(Config)

# creates the SQLAlchemy object
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db

# creates the Session object
# Session instance is not used for direct access, flask.session is used
Session(app)

# creates the MySQL instance
mysql = MySQL(app)

# creates the Bcrypt object
bcrypt = Bcrypt(app)

# creates the LoginManager object
login_manager = LoginManager(app)

# adds Flask_SocketIO to the flask application
socketio = SocketIO(app)

# creates the initial database
db.create_all()


class User(UserMixin):
    # pylint: disable=W0622
    def __init__(self, id, firstname, surname, username, email, password):
        self.id = id
        self.firstname = firstname
        self.surname = surname
        self.username = username
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    conn = mysql.connection
    curs = conn.cursor()

    curs.execute("""SELECT * FROM Users WHERE id = (%s);""",
                 [user_id])

    user = curs.fetchone()

    curs.close()

    if user is None:
        return None
    else:
        return User(*user[:-1])


"""
Routes
"""


@app.route('/')
def index():
    """
    GET: Landing page: index.html
    """
    return render_template("index.html")


@app.route('/play')
def play():
    """
    GET: Play page: play.html
    """
    return render_template('play.html')


@app.route('/game-pass-and-play')
def game_pass_and_play():
    """
    GET: Create instance of a chess Game, store it in session and display game-pass-and-play page
    """
    new_game = Game()
    session['game'] = new_game

    return render_template("game_pass_and_play.html")


@app.route('/game-ai')
def game_ai():
    """
    GET: Create instance of a chess Game, store it in session and display game-ai page
    """
    # get the depth query parameter
    depth = request.args.get('depth')

    if depth is None or not depth.isdigit or int(depth) not in [1, 2, 3]:
        return redirect(url_for('play'))

    new_game = Game_AI(int(depth))
    session['game'] = new_game

    return render_template("game_ai.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: Create a register form and return register page
    POST: Hash password and add user to database
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm(mysql)

    if form.validate_on_submit():
        # hashes the password and converts it using string
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        # establishes a connection
        conn = mysql.connection
        curs = conn.cursor()

        # inserts a row of data
        curs.execute("""INSERT INTO Users (firstname, surname, username, email, password) VALUES (%s,%s,%s,%s,%s);""",
                     [form.firstname.data, form.surname.data, form.username.data.lower(), form.email.data.lower(), hashed_password])

        # saves the changes
        conn.commit()
        # close connection
        curs.close()

        # flash sends a one-time alert
        flash(
            f'Account has been created! Welcome {form.firstname.data}!', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: Create a login form and return login page
    POST: Check if user exists then login in user
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        conn = mysql.connection
        curs = conn.cursor()

        curs.execute("""SELECT * FROM Users WHERE email = (%s);""",
                     [form.email.data])

        user = curs.fetchone()

        curs.close()

        if user is not None and bcrypt.check_password_hash(user[5], form.password.data):
            user = load_user(user[0])
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check your email and password.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


"""
SocketIO event handlers
"""


@socketio.on('socket_connect')
def connect():
    """Function that is run after a connection is established
    """
    # print('connected')


@socketio.on('available_moves')
def available_moves(move=None):
    """Emits all the legal moves in dictionary format, position dictionary, and game information.

    Args:
        move (str): the starting coord, ending coord, and special moves type value joined together as a string. The coordiantes are in algebraic notation.
        player_colour (tuple): player's colour as an integer.
    """
    # print(move, player_colour)
    game = session.get('game')

    if move is None:
        available_moves_dict = game.available_moves_dictionary()
    else:
        # executes move and returns available moves dictionary
        available_moves_dict = game.next_move(move)

        # print(game.chess)

    current_turn = game.current_turn
    winner = game.winner
    checkmate = game.is_checkmate
    draw = game.is_draw

    information = {'current_turn': current_turn,
                   'winner': winner, 'checkmate': checkmate, 'draw': draw}

    socketio.emit('available_moves_response', {
        'available_moves': available_moves_dict, 'position': game.position_dictionary(), 'information': information}, room=request.sid)


@socketio.on('ai_moves')
def ai_moves(player_colour):
    """AI makes next move and then emits all the legal moves in dictionary format, position dictionary, and game information.

    Args:
        player_colour (int): player's side colour
    """
    game = session.get('game')

    # before = time.time()
    ai_move = choice(minimax(game.chess, game.depth, player_colour))
    # print(f"Time: {time.time() - before}")

    ai_source = game.chess.coord_to_notation(ai_move[0])
    ai_target = game.chess.coord_to_notation(ai_move[1][0])
    ai_special_move = str(ai_move[1][1])

    if ai_special_move == "None":
        ai_special_move = ''

    # make that move
    game.next_move(ai_source + ai_target + ai_special_move)

    # print(f"TURN: {game.current_turn}")

    available_moves_dict = game.available_moves_dictionary()

    current_turn = game.current_turn
    winner = game.winner
    checkmate = game.is_checkmate
    draw = game.is_draw

    information = {'current_turn': current_turn,
                   'winner': winner, 'checkmate': checkmate, 'draw': draw}

    socketio.emit('available_moves_response', {
        'available_moves': available_moves_dict, 'position': game.position_dictionary(), 'information': information}, room=request.sid)

    # print('available_moves')


if __name__ == "__main__":
    socketio.run(app, debug=True)
