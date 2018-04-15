from Pyskell.Language.PyskellTypeSystem.AlgebraicDataType import *
from Pyskell.Language.Syntax import Syntax
from Pyskell.Language.TypeClasses import *
from Pyskell.Language.PyskellTypeSystem.TypeClass import *


"""
I want the ADT with the syntax of:
data.(...) >> d.Expr_0
            | d.Expr_1
            .
            .
            | d.Expr_n
(optional)  & deriving(...)
"""


class DerivingTypeClasses(Syntax):
    def __init__(self, *type_classes):
        super(DerivingTypeClasses, self).__init__("Syntax Error in deriving")
        for t in type_classes:
            if not issubclass(t, TypeClass):
                raise TypeError("Non type-class error {}".format(t))
        self.type_classes = type_classes


deriving = DerivingTypeClasses


class SyntaxDataConstructor(Syntax):
    """
    Basic Syntax Data Constructor containing `d.DataCon(...)` info
    """
    def __init__(self, data_con_name, args=(), t_classes=()):
        super(SyntaxDataConstructor, self).__init__("Syntax Error in DataCon")
        self.name = data_con_name
        self.args = args
        self.type_classes = t_classes


class SyntaxCalcDataConstructor(SyntaxDataConstructor):
    def __and__(self, other):
        if not isinstance(other, DerivingTypeClasses):
            raise self.invalid_syntax
        return SyntaxDerivedDataConstructor(self.name, self.args,
                                            other.type_classes)

    def __or__(self, other):
        if isinstance(other, SyntaxDataConstructor):
            d_cons = ((self.name, self.args), (other.name, other.args))
            if isinstance(other, SyntaxDerivedDataConstructor):
                return SyntaxDerivedDataConstructors(d_cons,
                                                     other.type_classes)
            return SyntaxDataConstructors(d_cons)
        raise self.invalid_syntax


class SyntaxBuildDataConstructor(SyntaxCalcDataConstructor):
    def __call__(self, *args):
        return SyntaxCalcDataConstructor(self.name, args)


class SyntaxDerivedDataConstructor(SyntaxDataConstructor):
    """
    This type is used to containing info for Data Constructor
    After the situation of Derived
    """
    pass


class SyntaxDerivedDataConstructors(Syntax):
    def __init__(self, data_constructors, classes=()):
        super(SyntaxDerivedDataConstructors, self)\
            .__init__("Syntax Error in `d`")
        self.data_constructors = data_constructors
        self.type_classes = classes


class SyntaxDataConstructors(SyntaxDerivedDataConstructors):
    def __init__(self, data_constructors):
        super(SyntaxDataConstructors, self).__init__(data_constructors)

    def __or__(self, other):
        if isinstance(other, SyntaxDataConstructor):
            d_con = ((other.name, other.args), )
            if isinstance(other, SyntaxDerivedDataConstructor):
                return SyntaxDerivedDataConstructors(
                    self.data_constructors + d_con,
                    other.type_classes)
            return SyntaxDataConstructors(self.data_constructors + d_con)
        raise self.invalid_syntax


class D(Syntax):
    def __init__(self):
        super(D, self).__init__("Error in Data Constructor")

    def __getattr__(self, item):
        if not str(item[0]).isupper():
            raise self.invalid_syntax
        return SyntaxBuildDataConstructor(item)


d = D()


class SyntaxTypeConstructor(Syntax):
    def __init__(self, t_name, t_args=()):
        super(SyntaxTypeConstructor, self).__init__("Error in TypeConstructor")
        self.name = t_name
        self.args = t_args

    def __eq__(self, other):
        if isinstance(other, SyntaxDataConstructor):
            return build_adt(self.name, self.args,
                             [(other.name, other.args)],
                             other.type_classes)
        elif isinstance(other, SyntaxDerivedDataConstructors):
            return build_adt(self.name, self.args,
                             other.data_constructors,
                             other.type_classes)
        raise self.invalid_syntax


class SyntaxCalledTypeConstructor(SyntaxTypeConstructor):
    def __call__(self, *args):
        if len(args) < 1:
            raise SyntaxError("Should not be data.{}()".format(self.name))
        if not all(type(arg) == str for arg in args):
            raise SyntaxError("Type Parameters Should be str hkt")
        if not all(arg.islower() for arg in args):
            raise SyntaxError("Type Parameters Should be lowercase")
        if len(args) != len(set(args)):
            raise SyntaxError("Type Parameters Should be Unique")
        return SyntaxHKTTypeConstructor(self.name, args)


class SyntaxHKTTypeConstructor(SyntaxTypeConstructor):
    pass


class Data(Syntax):
    def __init__(self):
        super(Data, self).__init__("Error in Type Constructor")

    def __getattr__(self, item):
        if not str(item[0]).isupper():
            raise self.invalid_syntax
        return SyntaxCalledTypeConstructor(item)


data = Data()
