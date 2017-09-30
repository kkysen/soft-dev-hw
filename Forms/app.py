from __future__ import print_function

import flask
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

app = Flask(__name__)


def redirect_url(route):
    # type: (callable) -> flask.Response
    return redirect(url_for(route.func_name))


@app.route('/login')
def login():
    # type: () -> str
    return render_template('form.jinja2')


@app.route('/auth', methods=['post'])
def authorize():
    # type: () -> flask.Response
    form = request.form
    username = form['username']
    password = form['password']
    print(username, password)
    return redirect_url(login)


@app.route('/')
def home():
    # type: () -> flask.Response
    return redirect_url(login)


if __name__ == '__main__':
    app.debug = True
    app.run()
