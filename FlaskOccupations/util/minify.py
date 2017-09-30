import bs4
import htmlmin
import flask


def prettify(html):
    # type: (str) -> str
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup.prettify()


def minify(app):
    # type: (flask.Flask) -> None
    wrapped = prettify if app.debug else htmlmin.minify

    @app.after_request
    def minifying_filter(response):
        # type: (flask.Response) -> flask.Response
        response.set_data(wrapped(response.get_data(as_text=True)))
        return response
