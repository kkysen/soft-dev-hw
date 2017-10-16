#!/usr/bin/python

"""
Khyber Sen and Jennifer Yu
SoftDev1 pd7
HW8 -- Do I Know You (Redirected)
2017-10-04
"""
from __future__ import print_function

import os

__author__ = 'Khyber Sen and Jennifer Yu'
__date__ = '2017-10-06'

from flask import Flask
from flask import Response
from flask import render_template
from flask import request
from flask import session
from werkzeug.datastructures import ImmutableMultiDict

from pprint import pprint

from util.flask_utils import reroute_to, preconditions, post_only
from util.template_context import context as ctx

app = Flask(__name__)

USERNAME_KEY = 'username'

users = {u'Hello': u'World'}


@app.reroute_from('/')
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
    if USERNAME_KEY in session:
        return reroute_to(welcome)
    else:
        return render_template('login.jinja2', **ctx)


def valid_account_form():
    # type: () -> bool
    return 'username' in request.form and 'password' in request.form


def get_account():
    # type: () -> (str, str)
    form = request.form  # type: ImmutableMultiDict
    return form['username'], form['password']


@app.route('/signup')
def signup():
    return render_template('signup.jinja2', **ctx)


@app.route('/add_user', methods=['get', 'post'])
@preconditions(signup, post_only, valid_account_form)
def add_user():
    username, password = get_account()
    users[username] = password
    pprint(users)
    return reroute_to(login)


def authenticate(username, password):
    # type: (str, str) -> str | None
    """Return None if authenicated or error msg if wrong."""
    if username not in users:
        return 'username'
    if password != users[username]:
        return 'password'
    return None


@app.route('/auth', methods=['get', 'post'])
@preconditions(login, post_only, valid_account_form)
def auth():
    # type: () -> Response
    """
    Authorize the user's attempted login and redirect them to the welcome page if successful.

    If the user enters the correct login info,
    add them to the session and redirect them to the welcome page,
    but if either the username or password were wrong,
    reload the same page with an error message on what they entered wrong.

    :return: the same login page with an error message or the welcome page
    """
    username, password = get_account()
    error = authenticate(username, password)
    if error:
        return render_template('login.jinja2', error=error, **ctx)
    session[USERNAME_KEY] = username
    return reroute_to(welcome)


@app.route('/welcome')
@preconditions(login, lambda: USERNAME_KEY in session)
def welcome():
    # type: () -> Response
    """
    Load the welcome page or redirect back to the login page if not logged in yet.

    :return: the welcome page or the redirected login page
    """
    username = session[USERNAME_KEY]
    return render_template('welcome.jinja2', username=username, **ctx)


@app.route('/logout')
def logout():
    # type: () -> Response
    """
    Logout the user by removing them from the session
    and redirect them back to the original login page.

    :return: the original login page
    """
    if USERNAME_KEY in session:
        del session[USERNAME_KEY]

    return reroute_to(login)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = os.urandom(32)
    app.run()
