#/usr/bin/python
"""

"""
import os
from flask import Flask, redirect
from flask.globals import request, session
from flask.templating import render_template
from clementine import Clementine


app = Flask(__name__)
app.secret_key = 'a5461ac7e021f24237b9f35e8f1acf35'

clementine = Clementine()


# Params
MUSIC_FOLDER = '/tmp/playcharm'
USERS = {'ivan': '12378'}


def auth(login):
    session['login'] = login
    return


def check_auth():
    return 'login' in session and len(session['login']) >= 0


@app.route("/", methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if login in USERS and USERS[login] == password:
            auth(login)
            return redirect('/player')
        return redirect('/')
    return render_template('main.html')


@app.route("/player", methods=['POST', 'GET'])
def player():
    if not check_auth():
        return redirect('/')

    if request.method == 'POST':
        req_file = request.files['file']
        if req_file:
            filename = req_file.filename
            req_file.save(os.path.join(MUSIC_FOLDER, filename))
            clementine.add_track('file:/' + MUSIC_FOLDER + '/' + filename, True)
            return redirect('player')
    return render_template('player.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
