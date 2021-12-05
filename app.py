from flask import Flask, render_template, session
from flask_session import Session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

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

# adds flask_socketio to the flask application
socketio = SocketIO(app)  # ,logger=True, engineio_logger=True

# creates the initial database
# db.create_all()


# Routes

@app.route('/')
def index():
    return "Home page"


@app.route('/game-offline')
def game():
    new_game = Game()
    session['game'] = new_game.serialise()
    return render_template("game.html")


# SocketIO event handlers

# Function that is run after a connection is established
@socketio.on('socket_connect')
def connect():
    print('connected')


# Emits all the legal moves in dictionary format
@socketio.on('available_moves')
def available_moves():
    game = deserialise(session.get('game'))
    socketio.emit('available_moves_response', {
        'available_moves': game.available_move_dictionary()})

    print('available_moves')
# , 'position': game.position_dictionary()


# Emits a piece and then returns all the legal moves in dictionary format
@socketio.on('next_move')
def next_move(move):
    # print(move)
    game = deserialise(session.get('game'))

    socketio.emit('available_moves_response', {
        'available_moves': game.next_move(move)})

    # Stores the updated game object into the session variable 'game'
    session['game'] = game.serialise()

    print(f"\n{game.chess}\n")
    print('next_move')


# Emits the chessboard configuration in dictionary format
@socketio.on('position')
def position():
    game = deserialise(session.get('game'))
    socketio.emit('position_response', {
                  'position': game.position_dictionary()})

    print('position')


# Emits all the information about the game
@socketio.on('information')
def information():
    game = deserialise(session.get('game'))

    current_turn = game.get_current_turn()
    winner = game.get_winner()
    checkmate = game.get_is_checkmate()
    draw = game.get_is_draw()

    information = {'current_turn': current_turn,
                   'winner': winner, 'checkmate': checkmate, 'draw': draw}

    socketio.emit('information_response', information)

    print('information')


if __name__ == "__main__":
    socketio.run(app, debug=True)


"""
# Joins the user to a room
@socketio.on('join')
def on_join_event(data):
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.emit('join_announcement', username +
                  ' has entered the room', to=room)

"""
