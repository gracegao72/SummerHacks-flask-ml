from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, Response
from flask_socketio import SocketIO

import random
import string
import logging
import json
import httplib2
import requests

from camera import Camera


########################################################################
#  App initialization
########################################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

########################################################################
#  Camera setup (i.e. this is for reading in the image)
########################################################################

camera = Camera()


########################################################################
#  Socket setup
#  This code sets up a network socket so a continuous stream of images
#  can be passed from the client to the server.
########################################################################

@socketio.on('input image', namespace='/test')
def test_message(input):
    input = input.split(",")[1]
    camera.enqueue_input(input)
    #camera.enqueue_input(base64_to_pil_image(input))

@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")


########################################################################
#  Index route
#  So when you go to localhost:5000/, this is the code that is called.
########################################################################

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

########################################################################
#  Video feed route
#  This is a route that gives you the processed image from the server.
#  When placed into the src attribute of an image tag, you get video.
########################################################################
def gen():
    """Video streaming generator function."""

    app.logger.info("starting to generate frames!")
    while True:
        frame = camera.get_frame() #pil_image_to_base64(camera.get_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

########################################################################
#  ML detection route
#  This is a route that gives you the ML detection result
#  By calling this route on a timer you can get a continous stream
########################################################################

# @app.route('/detection_feed')
# def detection_feed():
#     frame = camera.get_frame()
#     # process the image here
#     resp = {}
#     resp["hand_detection"] = True
#     resp["posture"] = "slouching"
#     return jsonify(resp)


########################################################################
#  Can ignore
########################################################################

if __name__ == "__main__":
    socketio.run(app)
