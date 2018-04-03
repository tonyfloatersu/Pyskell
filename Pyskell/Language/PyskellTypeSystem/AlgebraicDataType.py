"""
If there's ADT, then we might fly on the sky of types
We can carefully, and easily create a lot of types
"""

from TypeSignature import *


class ADT(OriginType):
    """
    Everything about ADT starts here
    """
    pass


def generate_type_constructor(name, type_args):
    def raise_error(whatever):
        raise whatever()
    default_attributes = {"__parameters__": tuple(type_args),
                          "__constraints__": ()}
    new_type = type(name, (ADT,), default_attributes)
    new_type.__type__ = lambda self: TypeOperator(new_type,
                                                  [TypeVariable()
                                                   for _ in type_args])
    new_type.__eq__ = lambda self, other: raise_error(TypeError)
    new_type.__ne__ = lambda self, other: raise_error(TypeError)
    new_type.__ge__ = lambda self, other: raise_error(TypeError)
    new_type.__le__ = lambda self, other: raise_error(TypeError)
    new_type.__lt__ = lambda self, other: raise_error(TypeError)
    new_type.__gt__ = lambda self, other: raise_error(TypeError)
    new_type.__mul__ = lambda self, other: raise_error(TypeError)
    new_type.__rmul__ = lambda self, other: raise_error(TypeError)
    new_type.__contains__ = lambda self, other: raise_error(TypeError)
    new_type.__add__ = lambda self, other: raise_error(TypeError)
    new_type.__radd__ = lambda self, other: raise_error(TypeError)
    new_type.__iter__ = lambda self, other: raise_error(TypeError)
    new_type.count = lambda self, other: raise_error(TypeError)
    new_type.index = lambda self, other: raise_error(TypeError)
    new_type.__repr__ = object.__repr__
    new_type.__str__ = object.__str__
    return new_type


def generate_data_constructor():
    pass
