from ..TypedFunc.TypeSignature import *
from ..TypedFunc.TypedFunction import TypedFunction
from collections import namedtuple


class ADT(OriginType):
    pass


def generate_type_constructor(name, type_args):

    def raise_fn(rua):
        raise rua()

    new_type = type(name, (ADT,),
                    {'__parameters__': tuple(type_args),
                     '__constructors__': ()})
    new_type.__type__ = lambda s: TypeOperator(new_type, [TypeVariable()
                                                          for _ in type_args])
    new_type.__iter__ = lambda self: raise_fn(TypeError)
    new_type.__contains__ = lambda self, other: raise_fn(TypeError)
    new_type.__add__ = lambda self, other: raise_fn(TypeError)
    new_type.__radd__ = lambda self, other: raise_fn(TypeError)
    new_type.__rmul__ = lambda self, other: raise_fn(TypeError)
    new_type.__mul__ = lambda self, other: raise_fn(TypeError)
    new_type.__lt__ = lambda self, other: raise_fn(TypeError)
    new_type.__gt__ = lambda self, other: raise_fn(TypeError)
    new_type.__le__ = lambda self, other: raise_fn(TypeError)
    new_type.__ge__ = lambda self, other: raise_fn(TypeError)
    new_type.__eq__ = lambda self, other: raise_fn(TypeError)
    new_type.__ne__ = lambda self, other: raise_fn(TypeError)
    new_type.count = lambda self, other: raise_fn(TypeError)
    new_type.index = lambda self, other: raise_fn(TypeError)
    new_type.__repr__ = object.__repr__
    new_type.__str__ = object.__str__
    return new_type


def generate_data_constructor(data_con_name, fields,
                              master_type_constructor,
                              slot_order_in_adt):

    base_class = namedtuple(data_con_name, ["i{}".format(i)
                                            for i, _ in enumerate(fields)])
    data_con_class = type(data_con_name, tuple([master_type_constructor,
                                                base_class]), {})
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
    """
    Create a new ADT
        typename str: name of type con
        type_args [str]
        data_constructors [(data_con_name (str), Signature)]
        to_derive [TypeClass]:

    Returns:
        The type constructor with data cons
    """

    adt_type = generate_type_constructor(typename, type_args)
    data_cons = [generate_data_constructor(dc_name, dc_field, adt_type, i)
                 for i, (dc_name, dc_field) in enumerate(data_constructors)]

    for type_class in to_derive:
        type_class.derive_instance(adt_type)

    for i, (dc_name, dc_fields) in enumerate(data_constructors):
        if len(dc_fields) == 0:
            continue
        return_adt_type = TypeSignatureHigherKind(adt_type, type_args)
        signature = TypeSignature([], list(dc_fields) + [return_adt_type])
        arg_ify_sig = type_sig_build(signature, {})
        data_cons[i] = TypedFunction(data_cons[i], arg_ify_sig,
                                     make_func_type(arg_ify_sig))

    return tuple([adt_type] + data_cons)
