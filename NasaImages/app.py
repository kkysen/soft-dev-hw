"""
Khyber Sen
SoftDev1 pd7
HW13 -- A RESTful Journey Skyward
2017-11-09
"""

__author__ = ['Khyber Sen']
__date__ = '2017-11-09'

import os

import requests
from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route('/')
def render_nasa_image():
    # type: () -> Response
    nasa_api_key = 'fcO1s8wiBu2ZqVp7AUac4BRRwS1RovmFJZ1C2S9F'
    url = 'https://api.nasa.gov/planetary/apod?api_key={}'.format(nasa_api_key)
    return render_template('nasa_image.jinja2', response=requests.get(url).json())


if __name__ == '__main__':
    app.debug = True
    app.secret_key = os.urandom(32)
    app.run()
