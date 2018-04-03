"""
If there's ADT, then we might fly on the sky of types
We can carefully, and easily create a lot of types
"""

from TypeSignature import *
from collections import namedtuple


class ADT(OriginType):
    """
    Everything about ADT starts here
    """
    pass


def generate_type_constructor(name, type_args):
    def raise_error(whatever):
        raise whatever()
    default_attributes = {"__parameters__": tuple(type_args),
                          "__constructors__": ()}
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


def generate_data_constructor(data_con_name, fields,
                              master_type_constructor,
                              slot_order_in_adt):
    base_class = namedtuple(data_con_name, ["i{}".format(i)
                                            for i, _ in enumerate(fields)])
    data_con_class = type(data_con_name, (master_type_constructor,
                                          base_class), {})
    data_con_class.__type_constructor__ = master_type_constructor
    data_con_class.__ADT__slot__order__ = slot_order_in_adt
    if len(fields) == 0:
        data_con_class = data_con_class()
    else:
        def a_list_of_types(self):
            type_args = [type_of(self[fields.index(k)])
                         if k in fields else TypeVariable()
                         for k in master_type_constructor.__parameters__]
            return TypeOperator(master_type_constructor, type_args)
        data_con_class.__type__ = a_list_of_types
    master_type_constructor.__constructors__ += (data_con_class,)
    return data_con_class


def build_adt(typename, type_args, data_constructors, to_derive):
    adt_type = generate_type_constructor(typename, type_args)
    data_cons = [generate_data_constructor(dc_name, dc_field, adt_type, i)
                 for i, (dc_name, dc_field) in enumerate(data_constructors)]

    # TODO: SOMETHING NEED TO BE DONE LATER
    return tuple([adt_type] + data_cons)
