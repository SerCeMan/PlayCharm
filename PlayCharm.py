#/usr/bin/python
"""

"""
import os
from flask import Flask
from flask.globals import request
from flask.templating import render_template
from clementine import Clementine


app = Flask(__name__)

clementine = Clementine()


# Params
MUSIC_FOLDER = '/tmp/playcharm'


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/player", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        req_file = request.files['file']
        if req_file:
            filename = req_file.filename
            req_file.save(os.path.join(MUSIC_FOLDER, filename))
            clementine.add_track('file:/' + MUSIC_FOLDER + '/' + filename, True)
    return render_template('player.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
