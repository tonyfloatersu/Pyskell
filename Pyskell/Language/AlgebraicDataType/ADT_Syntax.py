from .ADT import *
from ..Syntax import Syntax
from ..TypeClass.TypeClass import TypeClassMeta
from ..Syntax.Basic import Signature
from inspect import isclass


"""
I want the ADT with the syntax of:
@AlgebraDT(deriving=[...])
class SomeADT(...)
    Entry0: gT / t0 >> t1 >> td("SomeADT", ...)
    Entry1: gT / td("someADT", ...)
    Entry2: gT / t1 >> td("someADT", ...) >> td("someADT", ...)
    ...

How to get the entries... Still considering

Example:

@AlgebraDT(deriving=(Show, Eq))
class Tester(HigherKT("a", "b")):
    A_Entry: gT / int >> "a" >> "b"
    B_Entry: gT / str
    C_Entry: gT / td("Tester", "a", "b")

@AlgebraDT(None)
class BinT(HigherKT("a")):
    Empty: gT / td("BinT", "a")
    Leaf: gT / "a" >> td("BinT", "a")
    Node: gT / td("BinT", "a") >> td("BinT", "a") >> td("BinT", "a")
"""


class HigherKT(Syntax):

    def __init__(self, *args):
        super(HigherKT, self).__init__("Syntax Error in Higher Kinded Type")
        self.args = args


class ADTSigGen(Syntax):

    def __init__(self):
        super(ADTSigGen, self).__init__("Syntax Error in Type Signature")

    def __truediv__(self, other):
        return Signature((), []) >> other


gT = ADTSigGen()


def td(type_constructor, *parameters):

    if not isinstance(type_constructor, str):
        if not isclass(type_constructor):
            raise TypeError("Error in ADT Data Constructor, "
                            "type constructor not str or class")
        if not issubclass(type_constructor, ADT):
            raise TypeError("Error in ADT Data Constructor, "
                            "type constructor not str or class")
        if len(type_constructor.__parameters__) != len(parameters):
            raise TypeError("Incorrect number of type parameter {}"
                            .format(type_constructor.__name__))
    parameters = [i.signature if isinstance(i, Signature) else i
                  for i in parameters]
    return TypeSignatureHigherKind(type_constructor, parameters)


class AlgebraDT(Syntax):

    def __init__(self, deriving=None):
        super(AlgebraDT, self).__init__("Syntax Error in Algebra Syntax Type")
        if deriving is not None:
            for i in deriving:
                if not isinstance(i, TypeClassMeta):
                    raise TypeError(self.invalid_syntax)

    def __call__(self, cls):
        if not isinstance(cls, HigherKT):
            raise TypeError(self.invalid_syntax)
        name, obj_ls, cls_env = cls.args
        if len(obj_ls) is not 1:
            raise TypeError("Algebra dt must be inherited from HKT only")
        type_args = list(obj_ls[0].args)
        if len(type_args) != len(set(type_args)):
            raise SyntaxError("ADT no type con arg dup")
        for i in type_args:
            if not i.islower():
                raise TypeError("ADT type con only accept type variable")
        annotations = cls_env.get('__annotations__', {})
        for key, key_sig in annotations.items():
            if key[0].islower():
                raise SyntaxError("ADT Entry must not be lower case")
            if not isinstance(key_sig.signature.args[-1],
                              TypeSignatureHigherKind) or \
                key_sig.signature.args[-1].constructor != name or \
                    list(key_sig.signature.args[-1].parameters) \
                    != list(type_args):
                raise SyntaxError("ADT return res should be same as type con")
            for i in key_sig.signature.args:
                if isinstance(i, TypeSignatureHigherKind):
                    if isinstance(i.constructor, str):
                        if i.constructor != name:
                            raise TypeError("self name call error")
                        if len(i.parameters) != len(type_args):
                            raise TypeError("Incorrect number: type parameter")

        # ================= TEST SECTION ==================== #

        print(name)
        print(type_args)
        for key, val in annotations.items():
            print("{} {}".format(key, [(i.constructor, i.parameters)
                                       if isinstance(i, TypeSignatureHigherKind)
                                       else i
                                       for i in val.signature.args]))

        """

        data_constructors = [(key, annotations[key]) for key in annotations]

        t = build_ADT(typename=typename,
                      typeargs=typeargs,
                      data_constructors=data_constructors,
                      to_derive=deriving)
        res, *constructors = t

        for (constructor, value) in zip(annotations, constructors):
            setattr(res, constructor, value)
        setattr(res, 'enums', constructors)
        setattr(res, '__doc__', env.get('__doc__', ''))
        return res
        """
