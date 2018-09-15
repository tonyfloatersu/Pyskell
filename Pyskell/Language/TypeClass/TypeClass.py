from ..AlgebraicDataType import ADT
from ..TypedFunc.TypeSignature import OriginType, type_of
from ..HMTypeSystem import ListType
from collections import namedtuple


class TypeClassMeta(type):

    def __init__(cls, *args):
        super(TypeClassMeta, cls).__init__(*args)
        cls.__instances__ = {}
        # remove self, (... stay ...), remove TypeClass, remove object
        cls.__dependencies__ = cls.mro()[1: -2]

    def __getitem__(cls, item):
        try:
            if isinstance(item, ADT):
                return cls.__instances__[id(item.__type_constructor__)]
            elif isinstance(type_of(item), ListType):
                return cls.__instances__[id(type(item))]
            elif isinstance(item, OriginType):
                return cls.__instances__[id(type_of(item))]
            else:
                return cls.__instances__[id(type(item))]
        except KeyError:
            raise TypeError("No instance for {}".format(item))


class TypeClass(object, metaclass=TypeClassMeta):

    @classmethod
    def make_instance(cls, _type, **args):
        raise NotImplementedError("Type Classes must be implemented with "
                                  "make-instance")

    @classmethod
    def derive_instance(cls, _type):
        raise NotImplementedError("Type Classes must be implemented with "
                                  "derive-instance")


def add_instance(type_class, cls_tp, attributes):
    for dep in type_class.__dependencies__:
        if id(cls_tp) not in dep.__instances__:
            raise TypeError("No dependency {}".format(dep.__name__))

    instance_methods = namedtuple("__{}__".format(str(id(cls_tp))),
                                  attributes.keys())(**attributes)
    type_class.__instances__[id(cls_tp)] = instance_methods


def has_instance(cls_tp, type_class):
    if not issubclass(type_class, TypeClass):
        return False
    return id(cls_tp) in type_class.__instances__
