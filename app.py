import time
from flask import Flask, render_template, request, session, jsonify
import os
from letterGenerator import *
from flask_socketio import SocketIO, emit

chance_to_clean = 100
game_id_length = 5

app = Flask(__name__)
# app.secret_key = os.urandom(24)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)


currentGames = dict()

def cleanup():
    if randomChance(chance_to_clean):
        # print("CLEANING TIME")
        for key, val in currentGames.items():
            if abs(val["last_pinged"] - time.time()) > 5:
                del currentGames[key]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/creategame', methods=['POST', 'GET'])
def creategame():
    game_id =  id_generator(game_id_length)
    username = request.form.get('username')
    if (username == ""):
        username = "P1"
    #appending gameid to currentGames dictionary
    currentGames[game_id] = {"num_of_players": 1, "last_pinged": time.time(), "p1_name": username, "p2_name": None, "game_started": "false"}
    return render_template('game.html', name1 = username, game_id = game_id)

@app.route('/joingame', methods=['POST'])
def joingame():
    username = request.form.get('username')
    game_id = request.form.get('game-id')
    print(game_id)
    print(currentGames)
    if (username == ""):
        username = "P2"
    if game_id not in currentGames:
        return 'some error?'
    name1 = currentGames[game_id]["p1_name"]
    currentGames[game_id]["num_of_players"] = 2
    currentGames[game_id]["p2_name"] = username
    return render_template('game.html', name1 = name1, name2=username, game_id = game_id);

@app.route('/ping/<gameid>')
def pinged(gameid):
    if gameid not in currentGames:
        return 'some response'
    currentGames[gameid]['last_pinged'] = time.time()
    cleanup()
    return jsonify(currentGames[gameid])

@app.route('/startgame/<gameid>')
def startgame(gameid):
    if gameid not in currentGames:
        return 'some error'
    currentGames[gameid]["game_started"] = "true"

@app.route('/randomletters/<int:num>')
def randomletters(num):
    return generator(num)




if __name__ == '__main__':
    # socketio.run(app, debug=True)
    app.run(debug=True)
