from flask import Flask, render_template, request, session
import os
from letterGenerator import generator, id_generator
app = Flask(__name__)
app.secret_key = os.urandom(24)
game_id_length = 5

openGames = {"id":{}}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/creategame/', methods=['POST'])
def creategame():
    game_id = id_generator(game_id_length)
    while (game_id in openGames):
        game_id = id_generator(game_id_length)
    username = request.form.get('username')
    if (username == ""):
        username = "P1"
    return render_template('game.html', name = username, game_id=game_id)

@app.route('/randomletters/<int:num>')
def randomletters(num):
    return generator(num)

if __name__ == '__main__':
    app.run(debug=True)
