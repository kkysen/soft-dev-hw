#!/usr/bin/python

"""
Khyber Sen
SoftDev1 pd7
HW6 -- Echo Echo Echo
2017-10-02
"""
from __future__ import print_function

__author__ = 'Khyber Sen'
__date__ = '2017-10-02'

from flask import Flask
from flask import Response
from flask import render_template
from flask import request
from werkzeug.datastructures import ImmutableMultiDict

# noinspection PyUnresolvedReferences
import util.flask_utils

app = Flask(__name__)


def br(n):
    # type: (int) -> str
    return '<br>' * n


@app.redirect_from('/')
@app.route('/login')
def login():
    # type: () -> str
    return render_template('login.jinja2')


@app.route('/auth', methods=['post'])
def authorize():
    # type: () -> Response
    form = request.form  # type: ImmutableMultiDict
    username = form['username']
    password = form['password']
    print(username, password)
    return render_template(
        'after_login.jinja2',
        username=username,
        password=password,
        method=request.method,
        br=br,
    )


if __name__ == '__main__':
    app.debug = True
    app.run()
