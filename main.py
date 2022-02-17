import time

import cv2
import requests
import numpy as np
import pandas as pd
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def home():
    """Vide Streaming page"""
    return render_template('index.html')

def gen():
    """Video Streaming generator func """

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, img = cap.read()
        if ret:
            # img = cv2.imread(img)
            frame = cv2.imencode('.jpeg', img)[1].tobytes()
            yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n'
            time.sleep(0.1)
        else:
            break


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run('192.168.1.123',5000, debug=True)