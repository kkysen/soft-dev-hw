from __future__ import print_function

from flask import Flask
from flask import Response
from flask import render_template
from flask import request

from util.flask_utils import redirect_url

app = Flask(__name__)


@app.redirect_from('/')
@app.route('/login')
def login():
    # type: () -> str
    return render_template('form.jinja2')


@app.route('/auth', methods=['post'])
def authorize():
    # type: () -> Response
    form = request.form
    username = form['username']
    password = form['password']
    print(username, password)
    return redirect_url(login)


if __name__ == '__main__':
    app.debug = True
    app.run()
