import time
from flask import Flask, render_template, request, session, jsonify
import os
from letterGenerator import *
from flask_socketio import SocketIO, emit

chance_to_clean = 5
game_id_length = 5

app = Flask(__name__)
# app.secret_key = os.urandom(24)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)


currentGames = dict()

def cleanup():
    if randomChance(chance_to_clean):
        print("CLEANING TIME")
        for key, val in currentGames.items():
            if abs(val["last_pinged"] - time.time()) > 5:
                del currentGames[key]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/creategame/', methods=['POST'])
def creategame():
    game_id =  id_generator(game_id_length)
    username = request.form.get('username')
    if (username == ""):
        username = "P1"
    #appending gameid to currentGames dictionary
    currentGames[game_id] = {"num_of_players": 1, "last_pinged": time.time(), "p1_name": username, "p2_name": None}
    return render_template('game.html', name = username, game_id = game_id)

@app.route('/joingame/<gameid>')
def joingame(gameid):
    return

@app.route('/ping/<gameid>')
def pinged(gameid):
    print(currentGames)
    print(gameid)
    if gameid not in currentGames:
        return 'some response'
    currentGames[gameid]['last_pinged'] = time.time()
    cleanup()
    return jsonify(currentGames)

@app.route('/randomletters/<int:num>')
def randomletters(num):
    return generator(num)




if __name__ == '__main__':
    # socketio.run(app, debug=True)
    app.run(debug=True)
