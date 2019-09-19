from kafka import KafkaConsumer
from json import loads
import os
import cv2
import message
import numpy as np
from flask import Flask, Response, render_template, jsonify

topic = "test"


consumer = KafkaConsumer(
   'test',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-1',
    value_deserializer=lambda m: loads(m.decode('utf-8')),
    bootstrap_servers=['kafka:9093'])

consumer2 = KafkaConsumer(
   'test',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-1',
    value_deserializer=lambda m: loads(m.decode('utf-8')),
    bootstrap_servers=['kafka:9093'])
# Set the consumer in a Flask App
app = Flask(__name__)

@app.route('/', methods=['GET'])
def Index():
    """
    This is the heart of our video display. Notice we set the mimetype to
    multipart/x-mixed-replace. This tells Flask to replace any old images with
    new values streaming through the pipeline.
    """
    return render_template('index.html')
   # return Response(
    #    get_stream(),
     #   mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame(0)
        yield (b'--frame\r\n'
               b'Content-Type: images/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(get_stream(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video', methods=['GET'])
def video():
    """
    This is the heart of our video display. Notice we set the mimetype to
    multipart/x-mixed-replace. This tells Flask to replace any old images with
    new values streaming through the pipeline.
    """
    return Response(
        get_video_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame')


def get_stream():
    print('Listening...')

    for msg in consumer2:
        feed = msg.value.get("pix")
        b = bytes(feed, 'utf-8')
        print(feed)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + b + b'\r\n\r\n')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5001', debug=False)
