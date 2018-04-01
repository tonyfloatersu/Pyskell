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


class TypeVariable(object):
    """
    A type variable standing for an arbitrary type.
    NOT THREAD SAFE, ONLY UNDER SINGLE THREAD SITUATION

    All type variables have a unique id,
    but names are only assigned lazily, when required.
    """
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
    """n-ary type constructor which builds a new type"""

    def __init__(self, name, types):
        """initialize with name and n types to construct"""
        self.name = name
        self.types = types

    def __repr__(self):
        """representation with self type and constituent type"""
        if len(self.types) == 0:
            return show_type(self.name)
        return "({} {})".format(
            show_type(self.name), ' '.join(map(show_type, self.types)))


class Arrow(TypeOperator):
    """Bin-ary type constructor to build function types"""

    def __init__(self, from_type, to_type):
        super(self.__class__, self).__init__("->", [from_type, to_type])

    def __repr__(self):
        """represent with (a -> b) type"""
        return "({1} {0} {2})".format(
            show_type(self.name), *map(show_type, self.types))


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


class InferenceError(Exception):
    """If something goes wrong in HM TYPE SYS, raise this"""

    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message

    def __str__(self):
        return str(self.message)
