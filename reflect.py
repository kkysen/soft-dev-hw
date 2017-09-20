from flask import Flask
from flask import request
from urllib2 import urlopen

import randomizer

app = Flask(__name__)


@app.route('/')
def hello_world():
    # type: () -> str
    return 'Hello, World'


@app.route('/reflect')
def reflect():
    # type: (str) -> str
    url = request.query_string  # type: str
    try:
        http_request = urlopen(url)
    except ValueError:
        return 'bad url: ' + url
    result = http_request.read()  # type: str
    http_request.close()
    return result


@app.route('/hw')
def _hw1():
    return ''  # randomizer.main()


if __name__ == '__main__':
    app.run()
