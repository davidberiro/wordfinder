<<<<<<< HEAD
from flask import Flask, render_template, request
=======
from flask import Flask, render_template, request, session
import os
>>>>>>> de6c0adb9f30bc32360e851640f3e175c427be50

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('home.html')

<<<<<<< HEAD
@app.route('/creategame/', methods=['POST'])
def creategame():
    username = request.form.get('username')
    return render_template('game.html', name = username)
=======
@app.route('/creategame', methods=['POST'])
def creategame():
    username = request.form['username']
    return username
    
>>>>>>> de6c0adb9f30bc32360e851640f3e175c427be50

if __name__ == '__main__':
    app.run(debug=True)
