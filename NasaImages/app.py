"""
Khyber Sen
SoftDev1 pd7
HW13 -- A RESTful Journey Skyward
2017-11-11
"""

__author__ = ['Khyber Sen']
__date__ = '2017-11-11'

import os

import requests
from flask import Flask, Response, render_template

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/62.0.3202.89 Safari/537.36'

HTTP_HEADERS = {'User-Agent': USER_AGENT}

app = Flask(__name__)


@app.route('/nasa')
def render_nasa_image():
    # type: () -> Response
    nasa_api_key = 'fcO1s8wiBu2ZqVp7AUac4BRRwS1RovmFJZ1C2S9F'
    url = 'https://api.nasa.gov/planetary/apod?api_key={}'.format(nasa_api_key)
    return render_template('nasa_image.jinja2', response=requests.get(url).json())


def wikipedia_pages_query(*pages):
    # type: (list[str]) -> dict[unicode, unicode]
    url = 'https://en.wikipedia.org/w/api.php' \
          '?action=query' \
          '&titles={}' \
          '&prop=revisions' \
          '&rvlimit=1' \
          '&rvprop=content' \
          '&format=json'.format('|'.join(pages))
    data = requests.get(url, headers=HTTP_HEADERS).json()
    return {page['title']: page['revisions'][0]['*'] for page in data['query']['pages'].viewvalues()}


def wikipedia_parse_page(page):
    # type: (str) -> unicode
    url = 'https://en.wikipedia.org/w/api.php' \
          '?action=parse' \
          '&page={}' \
          '&prop=text' \
          '&contentformat=application/json' \
          '&contentmodel=json' \
          '&format=json'.format(page)
    data = requests.get(url, headers=HTTP_HEADERS).json()
    return data['parse']['text']['*'].replace('href="/', 'href="https://en.wikipedia.org/')


@app.route('/')
@app.route('/wikipedia')
def wikipedia():
    # type: () -> Response
    return render_template('wikipedia.jinja2', data=wikipedia_parse_page('NASA'))

 
if __name__ == '__main__':
    app.debug = True
    app.secret_key = os.urandom(32)
    app.run()
