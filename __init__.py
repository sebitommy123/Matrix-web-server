# serve.py

from threading import Thread
from flask import Flask, request
from flask import render_template
import json

subscribed = None
_width = 10
_height = 10
_channels = ["Main"]
_red = "Main"
_green = "Main"
_blue = "Main"
_cellSize = 10

# creates a Flask application, named app
app = Flask(__name__)

# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():
    return render_template('index.html', cellSize=_cellSize, width=_width, height=_height, channels=",".join([channel for channel in _channels]), red=_red, green=_green, blue=_blue)

@app.route("/pushMatrix", methods=['POST'])
def pushMatrix():
    
    matrix = json.loads(request.form["matrix"])

    if (subscribed is not None):
        subscribed(matrix)

    return "Ok"

def subscribe(func, simplify=False):
    global subscribed
    subscribed = func

    if simplify and len(_channels) == 1:
        subscribed = lambda matrix: func([[col[0] for col in row] for row in matrix])

def appRun():
    app.run(debug=False)

def start(width, height, cellSize, sync=False, debug=True, channels=["Main"], red="Main", green="Main", blue="Main"):
    global _width, _height, _channels, _red, _green, _blue, _cellSize

    _width = width
    _height = height
    _channels = channels
    _red = red
    _green = green
    _blue = blue
    _cellSize = cellSize

    print("Preparing to serve on localhost:5000")

    if not debug:
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
    
    if (sync):
        thread = Thread(target = appRun)
        thread.daemon = True
        thread.start()
    else:
        appRun()

    

