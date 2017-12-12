from flask import Flask, render_template, request, session
import os
from letterGenerator import generator, id_generator
from flask_socketio import SocketIO, emit

game_id_length = 5

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)


currentGames = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/creategame/', methods=['POST'])
def creategame():
    game_id =  id_generator(game_id_length)
    username = request.form.get('username')
    if (username == ""):
        username = "P1"
    return render_template('game.html', name = username, game_id = game_id)

@app.route('/joingame/<gameid>')
def joingame(gameid):
    return

@app.route('/randomletters/<int:num>')
def randomletters(num):
    return generator(num)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})
    print("hoohoo")

if __name__ == '__main__':
    socketio.run(app, debug=True)
