import inspect
import json

import os
from bson import json_util
from flask import Response, request, Flask, render_template
from typing import Any, Dict

from movies import Movies
from util.flask.flask_utils import reroute_to, preconditions, form_contains

app = Flask(__name__, static_url_path='')

movies = Movies()


@app.route('/')
def index():
    # type: () -> Response
    return render_template('index.html')


@app.route('/movies_queries', methods=['GET', 'POST'])
def movies_queries():
    # type: () -> Response
    return json.dumps(movies.queries())


@app.route('/bad', methods=['GET', 'POST'])
def bad_request():
    # type: () -> Response
    return Response(status=400, response='')  # HTTP 204 is Bad Request


@app.route('/movies', methods=['GET', 'POST'])
@preconditions(bad_request, form_contains('query'))
def query_movies():
    # type: () -> Response
    """
    Parse an $and query in the form of a dict[query method name, query args]
    in request.form['query'] and return the result of the mongo query.
    
    :return: jsonified Cursor from movies collection in Mongo DB
    """
    query = json.loads(request.form['query'])  # type: Dict[str, Any]
    print(query)
    for query_name, query_args in query.viewitems():
        query_func = getattr(movies, query_name, None)
        if query_func is None \
                or not hasattr(query_func, 'is_query')\
                or not isinstance(query_args, list)\
                or len(query_args) != len(inspect.getargspec(query_func).args) - 1:
            return reroute_to(bad_request)
    for query_name, query_args in query.viewitems():
        getattr(movies, query_name)(*query_args)
    return json_util.dumps(movies.fetch())


if __name__ == '__main__':
    reload_movies = True
    if reload_movies:
        movies.drop()
        movies.import_json_file()
    
    app.secret_key = os.urandom(32)
    app.run(debug=True)