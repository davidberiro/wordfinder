import time
from flask import Flask, render_template, request, session, jsonify
import os
from letterGenerator import *
from wordnik import *

#connecting to wordnik api
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '810e3e6d0084bc5c8200f024bb5062c4074589bfeba2e58f7'
client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)


chance_to_clean = 100
game_id_length = 5

app = Flask(__name__)

baseUrl = "http://api.wordnik.com/v4/word.json/"
api_key = "/api_key=810e3e6d0084bc5c8200f024bb5062c4074589bfeba2e58f7"

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
    currentGames[game_id] = {"num_of_players": 1, "last_pinged": time.time(), "p1_name": username, "p2_name": None, "game_started": "false",\
    "crossword": None, "submitted_words": {"p1": [], "p2": []}}
    return render_template('game.html', name1 = username, name2 = "P2", game_id = game_id)

@app.route('/joingame', methods=['POST'])
def joingame():
    username = request.form.get('username')
    game_id = request.form.get('game-id')
    if (username == ""):
        username = "P2"
    if game_id not in currentGames:
        return 'some error?'
    name1 = currentGames[game_id]["p1_name"]
    currentGames[game_id]["num_of_players"] = 2
    currentGames[game_id]["p2_name"] = username
    return render_template('game.html', name1 = name1, name2=username, game_id = game_id, player_num = "p2");

@app.route('/ping/<gameid>')
def pinged(gameid):
    if gameid not in currentGames:
        return 'some response'
    currentGames[gameid]['last_pinged'] = time.time()
    cleanup()
    return jsonify(currentGames[gameid])

@app.route('/pingforwords/<gameid>/<playerid>', methods=['POST'])
def pingforwords(gameid, playerid):
    if gameid not in currentGames:
        return 'some error'
    currentGames[gameid]['last_pinged'] = time.time()
    cleanup()
    words = request.json['words']
    currentGames[gameid]["submitted_words"][playerid] = words
    return jsonify(currentGames[gameid])


@app.route('/startgame/<gameid>')
def startgame(gameid):
    if gameid not in currentGames:
        return 'some error'
    currentGames[gameid]["game_started"] = "true"
    return jsonify(currentGames[gameid])

@app.route('/randomletters/<int:num>/<gameid>')
def randomletters(num, gameid):
    currentGames[gameid]["crossword"] = generator(num)
    return jsonify(currentGames[gameid])

@app.route('/checkword/<word>')
def checkword(word):
    if wordApi.getDefinitions(word) != None:
        return jsonify({"result": "true"})
    return jsonify({"result": "false"})

@app.route('/endgame/<gameid>')
def endgame(gameid):
    p1_word_list = currentGames[gameid]["submitted_words"]["p1"]
    p2_word_list = currentGames[gameid]["submitted_words"]["p2"]
    p1_dict = dict()
    p2_dict = dict()
    p1_points = 0
    p2_points = 0
    for word in p1_word_list:
        if wordApi.getDefinitions(word) != None:
            p1_points += len(word)
            p1_dict[word] = len(word)
        else:
            p1_dict[word] = 0
    for word in p2_word_list:
        if wordApi.getDefinitions(word) != None:
            p2_points += len(word)
            p2_dict[word] = len(word)
        else:
            p2_dict[word] = 0
    return jsonify({"p1": p1_dict, "p2": p2_dict, "p1_points": p1_points, "p2_points": p2_points})

    # print("p1 points: " + str(p1_points))
    # print("p2 points: " + str(p2_points))
    # if (p1_points>p2_points):
    #     return "P1 wins with " + str(p1_points) + "while P2 has " + str(p2_points)
    # else:
    #     return "P2 wins with " + str(p2_points) + "while P1 has " + str(p1_points)


if __name__ == '__main__':
    # socketio.run(app, debug=True)
    app.run(debug=True)
