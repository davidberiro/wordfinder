from flask import Flask, render_template, request, session
import os
from letterGenerator import generator
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/creategame/', methods=['POST'])
def creategame():
    username = request.form.get('username')
    return render_template('game.html', name = username)

@app.route('/randomletters/<int:num>')
def randomletters(num):
    return generator(num)

if __name__ == '__main__':
    app.run(debug=True)
