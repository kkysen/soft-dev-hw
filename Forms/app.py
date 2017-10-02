from __future__ import print_function

from flask import Flask
from flask import Response
from flask import render_template
from flask import request

# noinspection PyUnresolvedReferences
import util.flask_utils

app = Flask(__name__)


@app.redirect_from('/')
@app.route('/login')
def login():
    # type: () -> str
    return render_template('login.jinja2')


@app.route('/auth', methods=['post'])
def authorize():
    # type: () -> Response
    form = request.form
    print(form)
    username = form['username']
    password = form['password']
    print(username, password)
    return render_template(
        'after_login.jinja2',
        username=username,
        password=password,
        method=request.method)


if __name__ == '__main__':
    app.debug = True
    app.run()
