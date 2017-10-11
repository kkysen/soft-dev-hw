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


def repeat(s, n):
    # type: (str, int) -> str
    return s * n


def br(n):
    # type: (int) -> str
    """
    Concisely create many <br> tags.

    :param n: number of <br> to retur
    :return: n <br> tags
    """
    return repeat('<br>', n)


class TemplateVars(object):
    """
    TODO
    """

    def __init__(self):
        self.vars = {}

    def set(self, **kwargs):
        # type: (dict[str, any]) -> str
        self.vars.update(kwargs)
        return ''

    def get(self, name):
        # type: (str) -> any
        return self.vars[name]

    def get_safe(self, name, default=None):
        # type (str, any) -> any
        return self.vars.get(name, default)

    def add_to_context(self, context):
        # type: (dict[str, any]) -> dict[str, any]
        exported_methods = (self.set, self.get, self.get_safe)
        context.update({f.__func__.func_name: f for f in exported_methods})
        return context


TemplateVars.EXPORTED_METHODS = (
    TemplateVars.set,
    TemplateVars.get,
    TemplateVars.get_safe,
)


# Unfinished
class TemplateContext(object):
    def __init__(self):
        for exported_method in TemplateVars.EXPORTED_METHODS:
            self.__dict__[exported_method.__func__.func_name] = None

    def using_vars(self, template_vars):
        # type: (TemplateVars) -> None
        for exported_method in TemplateVars.EXPORTED_METHODS:
            func_name = exported_method.__func__.func_name
            self.__dict__[func_name] = template_vars.__dict__[func_name]

    @staticmethod
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

    @staticmethod
    def repeat(s, n):
        # type: (str, int) -> str
        return s * n

    @staticmethod
    def br(n):
        # type: (int) -> str
        """
        Concisely create many <br> tags.

        :param n: number of <br> to retur
        :return: n <br> tags
        """
        return TemplateContext.repeat('<br>', n)


TEMPLATE_FUNCTIONS = [
    if_else,
    repeat,
    br,
]

DEFAULT_TEMPLATE_CONTEXT = {}


def get_default_template_context(context):
    # type: (dict[str, any]) -> dict[str, any]
    """
    Get a new default template context with the given context added.

    :param context: the local context independent of default context
    :return: the combined local and default contexts
    """
    new_context = context.copy()
    new_context.update({f.func_name: f for f in TEMPLATE_FUNCTIONS})
    new_context.update(DEFAULT_TEMPLATE_CONTEXT)
    TemplateVars().add_to_context(new_context)
    return new_context