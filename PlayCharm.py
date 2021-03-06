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
USERS = {'ivan': '12378', 'stasx': '12351'}


def auth(login):
    session['login'] = login


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


@app.route("/play", methods=['POST'])
def play():
    clementine.play()
    return ''


@app.route('/playnum/<int:num>', methods=['POST'])
def play_num(num):
    clementine.play_num(num)
    return ''


@app.route("/pause", methods=['POST'])
def pause():
    clementine.pause()
    return ''


@app.route("/volume-up/<value>", methods=['POST'])
def volume_up(value):
    clementine.volume_up(value)
    return clementine.get_volume()


@app.route("/volume-down/<value>", methods=['POST'])
def volume_down(value):
    clementine.volume_down(value)
    return clementine.get_volume()


@app.route("/player", methods=['POST', 'GET'])
def player():
    if not check_auth():
        return redirect('/')

    if request.method == 'POST':
        #req_file = request.files['file']
        req_files = request.files.getlist("files")
        if req_files:
            for req_file in req_files:
                filename = req_file.filename
                req_file.save(os.path.join(MUSIC_FOLDER, filename))
                clementine.add_track('file:/' + MUSIC_FOLDER + '/' + filename, False)
        return redirect('player')
    return render_template('player.html', tracks=clementine.get_track_list(),
                           current_num=clementine.get_current_track_num(),
                           volume=clementine.get_volume())

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
