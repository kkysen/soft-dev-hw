#!/usr/bin/python

"""
Khyber Sen and Terry Guan
SoftDev1 pd7
HW7 -- Do I Know You
2017-10-04
"""
from __future__ import print_function

import os

__author__ = 'Khyber Sen and Terry Guan'
__date__ = '2017-10-02'

from flask import Flask
from flask import Response
from flask import render_template
from flask import request
from flask import session
from werkzeug.datastructures import ImmutableMultiDict

from util.flask_utils import redirect_url

app = Flask(__name__)

users = {'Hello': 'World'}


def br(n):
    # type: (int) -> str
    """
    Concisely create many <br> tags.

    :param n: number of <br> to retur
    :return: n <br> tags
    """
    return '<br>' * n


@app.redirect_from('/')
@app.route('/login')
def login():
    # type: () -> Response
    """
    Load the login page or redirect to the welcome page if already logged in.

    If the user hasn't logged in yet,
    load the login page for them to log in,
    but if the user has already logged in,
    redirect straight to the welcome page.

    :return: the login page or the welcome page redirection
    """
    if 'username' in session:
        print(session)
        return redirect_url(welcome)
    else:
        return render_template('login.jinja2')


@app.route('/auth', methods=['post'])
def authorize():
    # type: () -> Response
    """
    Authorize the user's attempted login and redirect them to the welcome page if successful.

    If the user enters the correct login info,
    add them to the session and redirect them to the welcome page,
    but if either the username or password were wrong,
    reload the same page with an error message on what they entered wrong.

    :return: the same login page with an error message or the welcome page
    """
    form = request.form  # type: ImmutableMultiDict
    username = form['username']
    password = form['password']
    if username not in users:
        return render_template('login.jinja2', failed='username')
    if password != users[username]:
        return render_template('login.jinja2', failed='password')
    session['username'] = username
    return redirect_url(welcome)


@app.route('/welcome')
def welcome():
    # type: () -> Response
    """
    Load the welcome page or redirect back to the login page if not logged in yet.

    :return: the welcome page or the redirected login page
    """
    if 'username' not in session:
        return redirect_url(login)
    username = session['username']
    return render_template('welcome.jinja2', username=username, br=br)


@app.route('/logout')
def logout():
    # type: () -> Response
    """
    Logout the user by removing them from the session
    and redirect them back to the original login page.

    :return: the original login page
    """
    del session['username']
    return redirect_url(login)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = os.urandom(32)
    app.run()
