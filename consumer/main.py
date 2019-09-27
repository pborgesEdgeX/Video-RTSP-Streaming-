# Define Imports
import base64
from json import loads

import cv2
import numpy as np
from flask import Flask, Response, render_template
from kafka import KafkaConsumer

W = 512
H = 288
# Define Kafka Topic
topic = "test"
# print(cv2.__version__)


# Instantiate Kafka Consumers
consumer = KafkaConsumer(
    'camera2',
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

# Instantiate Kafka Consumers
consumer3 = KafkaConsumer(
    'camera2',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-1',
    value_deserializer=lambda m: loads(m.decode('utf-8')),
    bootstrap_servers=['kafka:9093'])

consumer4 = KafkaConsumer(
    'test',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-1',
    value_deserializer=lambda m: loads(m.decode('utf-8')),
    bootstrap_servers=['kafka:9093'])

# Set the App to be Flask based
app = Flask(__name__)


# Route Index Page
@app.route('/', methods=['GET'])
def Index():
    """
    Using Jinja we are rendering a template page
    where it will call the get_stream() function
    """
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed2')
def video_feed2():
    return Response(get_stream2(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed3')
def video_feed3():
    return Response(get_stream3(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed4')
def video_feed4():
    return Response(get_stream4(), mimetype='multipart/x-mixed-replace; boundary=frame')


def get_stream():
    print('Listening to Feed 1...')
    for msg in consumer2:
        # Conversion: base-64 string --> array of bytes --> array of integers
        val = msg.value
        base64string = val['pix']  # pix is base-64 encoded string
        byteArray = base64.b64decode(base64string)  # byteArray is an array of bytes
        npArray = np.frombuffer(byteArray, np.uint8)  # npArray is an array of integers

        # Reshape array into an RGB image matrix of shape (channels, rows, cols)
        rows = val['rows']
        cols = val['cols']
        channels = val['channels']
        imgR = npArray[0::4].reshape((H, W))
        imgG = npArray[1::4].reshape((H, W))
        imgB = npArray[2::4].reshape((H, W))
        img = np.stack((imgR, imgG, imgB))
        img = np.moveaxis(img, 0, -1)
        print("ndim: ", img.ndim)
        print("shape:", img.shape)
        print("size: ", img.size)
        # print(img)
        success, a_numpy = cv2.imencode('.jpg', img)
        a = a_numpy.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + a + b'\r\n\r\n')


def get_stream2():
    print('Listening to Feed 2...')

    for msg in consumer:
        # Conversion: base-64 string --> array of bytes --> array of integers
        val = msg.value
        base64string = val['pix']  # pix is base-64 encoded string
        byteArray = base64.b64decode(base64string)  # byteArray is an array of bytes
        npArray = np.frombuffer(byteArray, np.uint8)  # npArray is an array of integers

        # Reshape array into an RGB image matrix of shape (channels, rows, cols)
        rows = val['rows']
        cols = val['cols']
        channels = val['channels']
        imgR = npArray[0::4].reshape((H, W))
        imgG = npArray[1::4].reshape((H, W))
        imgB = npArray[2::4].reshape((H, W))
        img = np.stack((imgR, imgG, imgB))
        img = np.moveaxis(img, 0, -1)
        print("ndim: ", img.ndim)
        print("shape:", img.shape)
        print("size: ", img.size)
        success, a_numpy = cv2.imencode('.jpg', img)
        a = a_numpy.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + a + b'\r\n\r\n')


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


def get_stream3():
    print('Listening to Feed 3...')

    for msg in consumer3:
        # Conversion: base-64 string --> array of bytes --> array of integers
        val = msg.value
        base64string = val['pix']  # pix is base-64 encoded string
        byteArray = base64.b64decode(base64string)  # byteArray is an array of bytes
        npArray = np.frombuffer(byteArray, np.uint8)  # npArray is an array of integers

        # Do something cool
        npArray = cv2.Canny(npArray, 350, 550)

        # Reshape array into an RGB image matrix of shape (channels, rows, cols)
        rows = val['rows']
        cols = val['cols']
        channels = val['channels']
        imgR = npArray[0::4].reshape((H, W))
        imgG = npArray[1::4].reshape((H, W))
        imgB = npArray[2::4].reshape((H, W))
        img = np.stack((imgR, imgG, imgB))
        img = np.moveaxis(img, 0, -1)
        success, a_numpy = cv2.imencode('.jpg', img)
        # edges = cv2.Canny(a_numpy,100,200)
        a = a_numpy.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + a + b'\r\n\r\n')


def get_stream4():
    print('Listening to Feed 4...')
    for msg in consumer4:
        # Conversion: base-64 string --> array of bytes --> array of integers
        val = msg.value
        base64string = val['pix']  # pix is base-64 encoded string
        byteArray = base64.b64decode(base64string)  # byteArray is an array of bytes
        npArray = np.frombuffer(byteArray, np.uint8)  # npArray is an array of integers

        # Reshape array into an RGB image matrix of shape (channels, rows, cols)
        rows = val['rows']
        cols = val['cols']
        channels = val['channels']
        imgR = npArray[0::4].reshape((H, W))
        imgG = npArray[1::4].reshape((H, W))
        imgB = npArray[2::4].reshape((H, W))
        img = np.stack((imgR, imgG, imgB))
        img = np.moveaxis(img, 0, -1)

        # Do something cool with RGB image
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # noise removal
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        # sure background area
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)
        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1
        # Now, mark the region of unknown with zero
        markers[unknown == 255] = 0

        markers = cv2.watershed(img, markers)
        img[markers == -1] = [255, 0, 0]

        success, a_numpy = cv2.imencode('.jpg', img)
        a = a_numpy.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + a + b'\r\n\r\n')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5001', debug=True)
