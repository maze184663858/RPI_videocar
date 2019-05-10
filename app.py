#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   appCam.py
#   based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
#   PiCam Local Web Server with Flask


# Raspberry Pi camera module (requires picamera package)
from flask import Flask, render_template, Response,request

from camera_pi import Camera
import RPi.GPIO as gpio
import Adafruit_DHT
import time

app = Flask(__name__)


in1=11
in2=12
in3=15
in4=16
gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(in1,gpio.OUT)
gpio.setup(in2,gpio.OUT)
gpio.setup(in3,gpio.OUT)
gpio.setup(in4,gpio.OUT)

gpio.output(in1,gpio.LOW)
gpio.output(in2,gpio.LOW)
gpio.output(in3,gpio.LOW)
gpio.output(in4,gpio.LOW)
def zuo():
    gpio.output(in1,gpio.HIGH)
    gpio.output(in2,gpio.LOW)
    gpio.output(in3,gpio.LOW)
    gpio.output(in4,gpio.LOW)
def you():
    gpio.output(in1,gpio.LOW)
    gpio.output(in2,gpio.LOW)
    gpio.output(in3,gpio.LOW)
    gpio.output(in4,gpio.HIGH)
def qian():
    gpio.output(in1,gpio.HIGH)
    gpio.output(in2,gpio.LOW)
    gpio.output(in3,gpio.LOW)
    gpio.output(in4,gpio.HIGH)
def hou():
    gpio.output(in1,gpio.LOW)
    gpio.output(in2,gpio.HIGH)
    gpio.output(in3,gpio.HIGH)
    gpio.output(in4,gpio.LOW)
def stop():
    gpio.output(in1,False)
    gpio.output(in2,False)
    gpio.output(in3,False)
    gpio.output(in4,False)

# get data from DHT sensor
def getDHTdata():       
    DHT22Sensor = Adafruit_DHT.DHT11
    gpio = 4
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, gpio)
    
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp)
    return temp, hum


@app.route("/",methods=['GET','POST'])
def index():
    timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    temp, hum = getDHTdata()
    
    templateData = {
      'time': timeNow,
      'temp': temp,
      'hum' : hum
    }


    a = request.form.get('k')
    if a=='w':
        print ('wwwwwwww')
        qian()      
    if a=='s':
        print('ssssssss')
        hou()
    if a=='d':
        print('dddddddd')
        you()
    if a=='a':
        print('aaaaaaaa')
        zuo()
    if a=='x':
        stop()
        print('ttttttttt')
    return render_template('index.html', **templateData)




def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port =8000,  threaded=True)
