"""
Types, identify yourself!
Even if you are a function/mono-type/monad!
"""
from Pyskell.Language.HMTypeSystem import *


class TypeSignatureError(Exception):
    pass


class TypeSignature(object):
    def __init__(self, constraints, args):
        self.constraints = constraints
        self.args = args


class TypeSignatureHigherKind(object):
    def __init__(self, t_constructor, t_parameters):
        self.constructor = t_constructor
        self.parameters = t_parameters


def make_func_type(type_para_list):
    if len(type_para_list) < 2:
        raise TypeSignatureError("Something's wrong in make func part.")
    elif len(type_para_list) == 2:
        return Arrow(type_para_list[0], type_para_list[1])
    else:
        return Arrow(type_para_list[0],
                     make_func_type(type_para_list[1:]))


def type_sig_arg_build(argument, constraints, type_var_dict):
    if isinstance(argument, list) and len(argument) == 1:
        return ListType(type_sig_arg_build(argument[0],
                                           constraints,
                                           type_var_dict))
    elif isinstance(argument, tuple):
        return TupleType(list(map(lambda x:
                                  type_sig_arg_build(x,
                                                     constraints,
                                                     type_var_dict),
                                  argument)))
    elif isinstance(argument, type):
        return TypeOperator(argument, [])
    elif isinstance(argument, str) and argument.islower():
        if argument not in type_var_dict:
            if argument in constraints:
                type_var_dict[argument] = \
                    TypeVariable(constraints=constraints[argument])
            else:
                type_var_dict[argument] = TypeVariable()
        return type_var_dict[argument]
    elif argument is None:
        return TypeOperator(None, [])
    # TODO: Higher kind / Sub Sig
    elif isinstance(argument, TypeSignature):
        """
        Due to the Syntax of Python, Tuple is used
        So I have to let function sig be another type signature
        """
        # return make_func_type(_)
        pass
    elif isinstance(argument, TypeSignatureHigherKind):
        pass
    raise TypeSignatureError(
        "Type Signature Fail to Build Argument: {}".format(argument)
    )
