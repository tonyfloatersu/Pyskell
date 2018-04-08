"""
Types, identify yourself!
Even if you are a function/mono-type/monad!
It's somewhat about static type and Py-skell layer of type
"""
from Pyskell.Language.HMTypeSystem import *
import types

__python_builtins__ = {
    types.BooleanType, types.BufferType, types.BuiltinFunctionType,
    types.BuiltinMethodType, types.ClassType, types.CodeType,
    types.ComplexType, types.DictProxyType, types.DictType,
    types.DictionaryType, types.EllipsisType, types.FileType,
    types.FloatType, types.FrameType, types.FunctionType,
    types.GeneratorType, types.GetSetDescriptorType, types.InstanceType,
    types.IntType, types.LambdaType, types.ListType, types.LongType,
    types.MemberDescriptorType, types.MethodType, types.ModuleType,
    types.NoneType, types.NotImplementedType, types.ObjectType,
    types.SliceType, types.StringType, types.StringTypes,
    types.TracebackType, types.TupleType, types.TypeType,
    types.UnboundMethodType, types.UnicodeType, types.XRangeType, set,
    frozenset}


def is_builtin_type(some_type):
    return some_type in __python_builtins__


__python_function_types__ = {
    types.FunctionType, types.LambdaType, types.MethodType,
    types.UnboundMethodType, types.BuiltinFunctionType,
    types.BuiltinMethodType}


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


def make_func_type(type_para_list):
    if len(type_para_list) < 2:
        raise TypeSignatureError("Something's wrong in make func part.")
    elif len(type_para_list) == 2:
        return Arrow(type_para_list[0], type_para_list[1])
    else:
        return Arrow(type_para_list[0],
                     make_func_type(type_para_list[1:]))


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
        """
        Due to the Syntax of Python, Tuple is used
        So I have to let function sig be another type signature
        """
        return make_func_type(type_sig_build(argument, type_var_dict))
    elif isinstance(argument, TypeSignatureHigherKind):
        if type(argument.constructor) is str:
            higher_kind = type_sig_arg_build(argument.constructor,
                                             constraints,
                                             type_var_dict)
        else:
            higher_kind = argument.constructor
        return TypeOperator(higher_kind,
                            list(map(lambda x:
                                     type_sig_arg_build(x,
                                                        constraints,
                                                        type_var_dict),
                                     argument.parameters)))
    elif argument is None:
        return TypeOperator(None, [])
    elif isinstance(argument, list) and len(argument) == 1:
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
    raise TypeSignatureError(
        "Type Signature Fail to Build Argument: {}".format(argument)
    )


def type_sig_build(type_sig, type_var_dict=None):
    args, constraints = type_sig.args, type_sig.constraints
    type_var_dict = {} if type_var_dict is None else type_var_dict
    return list(map(lambda x:
                    type_sig_arg_build(x, constraints, type_var_dict),
                    args))


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
