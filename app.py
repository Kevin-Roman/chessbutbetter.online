import sqlite3
import time
from random import choice

from flask import Flask, flash, redirect, render_template, session, url_for
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from ai import minimax
from forms import LoginForm, RegistrationForm
from game import Game, deserialise

# creates the Flask instance
app = Flask(__name__)

# secret key that will be used for securely signing the session cookie
app.config['SECRET_KEY'] = "mysecretkey"

# specifies which type of session interface to use
app.config['SESSION_TYPE'] = 'sqlalchemy'

# the database URI that should be used for the connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sessiondb.sqlite3'

# Flask-SQLAlchemy will not track modifications of objects and emit signals
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# creates the SQLAlchemy object
db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

# creates the Session object
# Session instance is not used for direct access, flask.session is used
Session(app)

# creates the Bcrypt object
bcrypt = Bcrypt(app)

# adds flask_socketio to the flask application
socketio = SocketIO(app)  # ,logger=True, engineio_logger=True

# creates the initial database
# db.create_all()


# Routes

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game-pass-and-play')
def game_pass_and_play():
    new_game = Game()
    session['game'] = new_game.serialise()
    return render_template("game_pass_and_play.html")


@app.route('/game-ai')
def game_ai():
    new_game = Game()
    session['game'] = new_game.serialise()

    return render_template("game_ai.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # hashes the password and converts it using string
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        # establishes a connection
        conn = sqlite3.connect('./accounts.db')
        curs = conn.cursor()

        # inserts a row of data
        curs.execute("INSERT INTO Users (firstname, surname, username, email, password) VALUES (?,?,?,?,?);",
                     [form.firstname.data, form.surname.data, form.username.data.lower(), form.email.data.lower(), hashed_password])

        # saves the changes
        conn.commit()
        # close connection
        conn.close()

        # flash sends a one-time alert
        flash(
            f'Account has been created! Welcome {form.firstname.data}!', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


# SocketIO event handlers

# Function that is run after a connection is established
@socketio.on('socket_connect')
def connect():
    print('connected')


# Emits all the legal moves in dictionary format, position dictionary, and game information. Also executes the computer's move if playing AI gamemode.
@socketio.on('available_moves')
def available_moves(move=None, ai_info=None):
    game = deserialise(session.get('game'))

    if move is None:
        available_moves_dict = game.available_move_dictionary()
    else:
        # print(f"\n\n{move}\n\n")
        available_moves_dict = game.next_move(move)

        print(game.chess)

    current_turn = game.get_current_turn()
    winner = game.get_winner()
    checkmate = game.get_is_checkmate()
    draw = game.get_is_draw()

    information = {'current_turn': current_turn,
                   'winner': winner, 'checkmate': checkmate, 'draw': draw}

    socketio.emit('available_moves_response', {
        'available_moves': available_moves_dict, 'position': game.position_dictionary(), 'information': information})

    if ai_info is not None and not checkmate and not draw:
        depth, player_colour = ai_info

        before = time.time()
        ai_move = choice(minimax(game.chess, depth, player_colour))
        print(f"Time: {time.time() - before}")

        ai_source = game.chess.coord_to_notation(ai_move[0])
        ai_target = game.chess.coord_to_notation(ai_move[1][0])
        ai_special_move = str(ai_move[1][1])

        if ai_special_move == "None":
            ai_special_move = ''

        # make that move
        game.next_move(ai_source + ai_target + ai_special_move)

        available_moves_dict = game.available_move_dictionary()

        current_turn = game.get_current_turn()
        winner = game.get_winner()
        checkmate = game.get_is_checkmate()
        draw = game.get_is_draw()

        information = {'current_turn': current_turn,
                       'winner': winner, 'checkmate': checkmate, 'draw': draw}

        socketio.emit('available_moves_response', {
            'available_moves': available_moves_dict, 'position': game.position_dictionary(), 'information': information})

    session['game'] = game.serialise()

    print('available_moves')


if __name__ == "__main__":
    clear_tables = False

    if clear_tables:
        conn = sqlite3.connect("accounts.db")
        cur = conn.cursor()
        # pylint: disable=W1514
        with open('schema.sql') as schema:
            cur.executescript(schema.read())
        conn.commit()

    socketio.run(app, debug=True)
