from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/creategame/', methods=['POST'])
def creategame():
    username = request.form.get('username')
    return render_template('game.html', name = username)

if __name__ == '__main__':
    app.run(debug=True)
