"""
Acknowledge:
    Inspired by the following link:
    http://smallshire.org.uk/sufficientlysmall/2010/04/11/a-hindley-milner-type-inference-implementation-in-python/
BASIC KNOWLEDGE REQUIREMENT:
    https://en.wikipedia.org/wiki/Hindley%E2%80%93Milner_type_system
"""


"""
ABT REQUIRED ELEMENTS
(Abstract Binding Tree)
"""


class Lambda(object):
    """Lambda re-defined"""
    def __init__(self, args, exec_body):
        """initialize with args and exec_body"""
        self.args = args
        self.exec_body = exec_body

    def __str__(self):
        """representation"""
        return "(\{} -> {})".format(self.args, self.exec_body)


class Let(object):
    """Let expression be replace in environment expression"""
    def __init__(self, expr, rep, env_expr):
        """initialize with expression, replacement and env expression"""
        self.expr = expr
        self.rep = rep
        self.env_expr = env_expr

    def __str__(self):
        """representation"""
        return "(let {} = {} in {})".format(self.expr,
                                            self.rep,
                                            self.env_expr)


class FunctionApplication(object):
    """apply function to variable"""
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __str__(self):
        """representation"""
        return "({} {})".format(self.func, self.args)


class Variable(object):
    """variable re-define"""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        """representation"""
        return str(self.name)


"""
TYPE MANIPULATE
"""


def show_type(type_name):
    """
    Func: Show Type:
    if type_name is a type, then return its string, else try to return itself
    The final condition is to return str(type_name)
    """
    if isinstance(type_name, str):
        return type_name
    elif isinstance(type_name, type):
        return type_name.__name__
    return str(type_name)


"""
THE FOLLOWING FUNCTION IS NOT THREAD SAFE
PLEASE USE ONLY UNDER SINGLE THREAD SITUATION
"""


class TypeVariable(object):
    """
    A type variable standing for an arbitrary type.

    All type variables have a unique id, but names are only assigned lazily,
    when required.
    """
    __next_var_id__ = 0
    __next_var_name__ = 'a'

    def __init__(self):
        self.id = self.__next_var_id__
        self.__next_var_id__ += 1


class TypeOperator(object):
    """n-ary type constructor which builds a new type"""
    def __init__(self, name, types):
        """initialize with name and n types to construct"""
        self.name = name
        self.types = types

    def __repr__(self):
        """representation with self type and constituent type"""
        if len(self.types) == 0:
            return show_type(self.name)
        return "({} {})".format(show_type(self.name),
                                ' '.join(map(show_type, self.types)))


class Function(TypeOperator):
    """Bin-ary type constructor to build function types"""
    def __init__(self, from_type, to_type):
        super(self.__class__, self).__init__("->", [from_type, to_type])

    def __repr__(self):
        """represent with (a -> b) type"""
        return "({1} {0} {2})".format(show_type(self.name),
                                      *map(show_type, self.types))


class TupleType(TypeOperator):
    """N-ary constructor which builds tuple types"""
    def __init__(self, types):
        """call TypeOperator typename tuple and type list"""
        super(self.__class__, self).__init__(tuple, types)

    def __repr__(self):
        """show in (a_i ... a_j) format"""
        return "({})".format(", ".join(map(show_type, self.types)))


class ListType(TypeOperator):
    """Unary constructor which builds list types"""
    def __init__(self, list_type):
        """
        call TypeOperator typename []
         (python list is very easy on type, but this list is strong type)
        and types with only [list_type]
        """
        super(self.__class__, self).__init__("[]", [list_type])

    def __repr__(self):
        """represent with [type]"""
        return "[{}]".format(show_type(self.types[0]))
