class Variable(object):
    """variable re-define"""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{}".format(str(self.name))


class FuncApp(object):
    """apply function to variable"""
    def __init__(self, expr_func, expr_arg):
        self.expr_func = expr_func
        self.expr_arg = expr_arg

    def __str__(self):
        """representation"""
        return "({} {})".format(self.expr_func, self.expr_arg)


class Lambda(object):
    """Lambda re-defined"""
    def __init__(self, name_arg, expr_body):
        """initialize with args and exec_body"""
        self.name = name_arg
        self.expr_body = expr_body

    def __str__(self):
        """representation"""
        return "(\{} -> {})".format(self.name, self.expr_body)


class Let(object):
    """Let expression be replace in environment expression"""
    def __init__(self, name_replaced, expr_replacement, expr):
        """initialize with expression, replacement and env expression"""
        self.name_replaced = name_replaced
        self.expr_replacement = expr_replacement
        self.expr = expr

    def __str__(self):
        """representation"""
        return "(let {} = {} in {})".format(self.name_replaced,
                                            self.expr_replacement,
                                            self.expr)
