#!/usr/bin/python

"""
Khyber Sen and Michael Ruvinshteyn
SoftDev1 pd7
HW5 -- Jinja Tuning
2017-09-26
"""

__author__ = 'Khyber Sen'
__date__ = '2017-09-22'

from flask import Flask
from flask import render_template

# noinspection PyUnresolvedReferences
import util.flask_utils

try:
    from flask_compress import Compress
except ImportError:
    import subprocess

    # since flask_compress isnt' installed yet, explicitly install it now
    subprocess.call('pip install flask-compress', shell=True)
    from flask_compress import Compress

from util.occupations import Occupations

occupations = Occupations.in_united_states()

app = Flask(__name__)


def if_else(first, a, b):
    # type: (bool, any, any) -> any
    """
    Functional equivalent of conditional expression.

    :param first: True or False
    :param a: to be returned if first is True
    :param b: to be returned if first is False
    :return: a if first else b
    """
    return a if first else b


@app.redirect_from('/')
@app.route('/occupations')
def render_occupations():
    # type: () -> str
    """
    Render the occupations.jinja2 template.

    title: the title of the webpage
    occupations: the Occupations object
    chosen_occupation: the randomly-selected Occupation
    chosen_first: if the chosen_occupation section should appear first in the HTML
    if_else: shortcut for the lengthy if else statements in jinja templates

    :return: the rendered template
    """
    return render_template(
        'occupations.jinja2',
        title='US Occupations',
        occupations=occupations,
        chosen_occupation=occupations.random_occupation(),
        chosen_first=True,
        if_else=if_else,
    )


if __name__ == '__main__':
    app.debug = True
    # minify(app)
    Compress(app)
    app.run()
