from ..HMTypeSystem import *
from ..AlgoW import *
import types

__python_builtins__ = {
    type, bool, dict, float, int, str, tuple, complex, type(None), list, set,
    type(Ellipsis), types.BuiltinFunctionType, types.BuiltinMethodType,
    types.CodeType, types.DynamicClassAttribute, types.FrameType,
    types.FunctionType, types.GeneratorType, types.GetSetDescriptorType,
    types.LambdaType, types.MappingProxyType, types.MemberDescriptorType,
    types.MethodType, types.TracebackType
}


def is_builtin_type(some_type):
    return some_type in __python_builtins__


__python_function_types__ = {
    types.FunctionType, types.LambdaType, types.MethodType,
    types.BuiltinFunctionType, types.BuiltinMethodType
}


def is_py_func_type(some_type):
    return some_type in __python_function_types__


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

# old version


def make_func_type(type_para_list):
    if len(type_para_list) < 2:
        raise TypeSignatureError("Something's wrong in make func part.")
    elif len(type_para_list) == 2:
        return Arrow(type_para_list[0], type_para_list[1])
    else:
        return Arrow(type_para_list[0],
                     make_func_type(type_para_list[1:]))

# new version


def make_type(type_para_list):
    if len(type_para_list) == 0:
        raise TypeSignatureError("Type Signature Parameter List Length 0 Error")
    if any(map(lambda x: not isinstance(x, Type), type_para_list)):
        raise TypeSignatureError("Type Signature Parameter List Member Error")

    def make_type_inner(tp_list):
        return tp_list[0] if len(tp_list) == 1 else \
            TArrow(tp_list[0], make_type_inner(tp_list[1:]))

    return make_type_inner(type_para_list)


# old version


def type_sig_arg_build(argument, constraints, type_var_dict):
    if isinstance(argument, str) and argument.islower():
        if argument not in type_var_dict:
            if argument in constraints:
                type_var_dict[argument] = \
                    TypeVariable(constraints=constraints[argument])
            else:
                type_var_dict[argument] = TypeVariable()
        return type_var_dict[argument]
    elif isinstance(argument, TypeSignature):
        return make_func_type(type_sig_build(argument, type_var_dict))
    elif isinstance(argument, TypeSignatureHigherKind):
        higher_kind = type_sig_arg_build(argument.constructor, constraints,
                                         type_var_dict) \
            if type(argument.constructor) is str \
            else argument.constructor
        return TypeOperator(higher_kind,
                            [type_sig_arg_build(x, constraints, type_var_dict)
                             for x in argument.parameters])
    elif argument is None:
        return TypeOperator(None, [])
    elif isinstance(argument, list) and len(argument) == 1:
        return ListType(type_sig_arg_build(argument[0], constraints,
                                           type_var_dict))
    elif isinstance(argument, tuple):
        return TupleType([type_sig_arg_build(x, constraints, type_var_dict)
                          for x in argument])
    elif isinstance(argument, type):
        return TypeOperator(argument, [])
    raise TypeSignatureError(
        "Type Signature Fail to Build Argument: {}".format(argument)
    )


# new version

def ts_args(argument, constraint):
    if isinstance(argument, str) and argument.islower():
        pass
    # TODO: need to redesign how to build type signature arguments


def type_sig_build(type_sig, type_var_dict=None):
    args, constraints = type_sig.args, type_sig.constraints
    type_var_dict = {} if type_var_dict is None else type_var_dict
    return [type_sig_arg_build(x, constraints, type_var_dict) for x in args]


class PythonFunctionType(object):
    pass


class OriginType(object):
    """
    Everything starts at this type in Pyskell
    """
    def __type__(self):
        raise TypeError("You touch something you should never touch\n"
                        "THIS IS ORIGIN TYPE, EVERYTHING STARTS HERE")


class Undefined(OriginType):
    def __type__(self):
        return TypeVariable()


def type_of(unknown_type):
    TypeVariable.next_var_name = 0
    if isinstance(unknown_type, OriginType):
        return unknown_type.__type__()
    elif isinstance(unknown_type, tuple):
        return TupleType(list(map(type_of, unknown_type)))
    elif unknown_type is None:
        return TypeOperator(None, [])
    elif type(unknown_type) in __python_function_types__:
        return TypeOperator(PythonFunctionType, [])
    return TypeOperator(type(unknown_type), [])
