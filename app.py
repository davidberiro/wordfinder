from flask import Flask, render_template, request, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/creategame', methods=['POST'])
def creategame():
    username = request.form['username']
    return username
    

if __name__ == '__main__':
    app.run(debug=True)
