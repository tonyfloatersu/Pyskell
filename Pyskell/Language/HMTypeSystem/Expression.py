class Variable(object):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{}".format(str(self.name))


class FuncApp(object):

    def __init__(self, expr_func, expr_arg):
        self.expr_func = expr_func
        self.expr_arg = expr_arg

    def __str__(self):
        return "({} {})".format(self.expr_func, self.expr_arg)


class Lambda(object):

    def __init__(self, name_arg, expr_body):
        self.name = name_arg
        self.expr_body = expr_body

    def __str__(self):
        return "(\{} -> {})".format(self.name, self.expr_body)


class Let(object):

    def __init__(self, name_replaced, expr_replacement, expr):
        self.name_replaced = name_replaced
        self.expr_replacement = expr_replacement
        self.expr = expr

    def __str__(self):
        return "(let {} = {} in {})".format(self.name_replaced,
                                            self.expr_replacement,
                                            self.expr)


def show_type(type_name):

    if isinstance(type_name, str):
        return type_name
    elif isinstance(type_name, type):
        return type_name.__name__
    return str(type_name)


class TypeVariable(object):

    __next_var_id = 0
    next_var_name = 0

    def __init__(self, constraints=()):
        self.id = self.__next_var_id
        TypeVariable.__next_var_id += 1
        self.constraints = constraints
        self.__name = None
        self.instance = None

    def __generate_name(self):
        if self.__name is None:
            self.__name = "a" + str(self.next_var_name)
            TypeVariable.next_var_name += 1
        return self.__name

    @property
    def name(self):
        return self.__generate_name()

    def __str__(self):
        if self.instance is not None:
            return str(self.instance)
        return self.name

    def __repr__(self):
        return "TypeVariable(id = {0})".format(self.id)


class TypeOperator(object):

    def __init__(self, name, types):
        self.name = name
        self.types = types

    def __repr__(self):
        if len(self.types) == 0:
            return show_type(self.name)
        return "({} {})".format(
            show_type(self.name), ' '.join(map(show_type, self.types)))


class Arrow(TypeOperator):

    def __init__(self, from_type, to_type):
        super().__init__("->", [from_type, to_type])

    def __repr__(self):
        return "({1} {0} {2})".format(
            show_type(self.name), *map(show_type, self.types))


class TupleType(TypeOperator):

    def __init__(self, types):
        super().__init__(tuple, types)

    def __repr__(self):
        return "({})".format(", ".join(map(show_type, self.types)))


class ListType(TypeOperator):

    def __init__(self, list_type):
        super().__init__("[]", [list_type])

    def __repr__(self):
        return "[{}]".format(show_type(self.types[0]))


class InferenceError(Exception):

    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message

    def __str__(self):
        return str(self.message)
