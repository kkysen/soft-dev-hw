from flask import Flask
from flask import Response
from flask import redirect
from flask import url_for


def redirect_url(route):
    # type: (callable) -> Response
    return redirect(url_for(route.func_name))


def redirect_from(app, rule, **options):
    # type: (Flask, str, dict[str, any]) -> callable
    """
    Redirect the given rule and options to the route it is decorating.

    :param app: this app
    :param rule: rule from @app.route
    :param options: options from @app.route
    :return: a decorator that adds the redirecting logic
    """

    def decorator(func_to_redirect):
        # type: (callable) -> callable
        """
        Decorate a route function to add another route that redirects to this one.

        :param func_to_redirect: the route function to redirect
        :return: the original func_to_redirect
        """

        def redirector():
            # type: () -> Response
            """
            The actual route function that accomplishes the redirecting.

            :return: the redirected Response
            """
            return redirect_url(func_to_redirect)

        # uniquely modify the redirector name
        # so @app.route will have a unique function name
        # the next time redirect_from is called
        redirector.func_name += '_for_' + func_to_redirect.func_name
        app.route(rule, **options)(redirector)

        return func_to_redirect

    return decorator


# extension method
Flask.redirect_from = redirect_from
del redirect_from
