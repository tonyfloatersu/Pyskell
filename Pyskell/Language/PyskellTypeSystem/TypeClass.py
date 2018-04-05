from AlgebraicDataType import ADT
from TypeSignature import OriginType, type_of
from Pyskell.Language.HMTypeSystem import ListType
from collections import namedtuple


class TypeClassMeta(type):
    def __init__(cls, *args):
        super(TypeClassMeta, cls).__init__(*args)
        cls.__instances__ = {}
        cls.__dependencies__ = cls.mro()[1: -2]

    def __getitem__(self, item):
        try:
            if isinstance(item, ADT):
                return self.__instances__[id(item.__type_constructor__)]
            elif isinstance(type_of(item), ListType):
                return self.__instances__[id(type(item))]
            elif isinstance(item, OriginType):
                return self.__instances__[id(type_of(item))]
            else:
                return self.__instances__[id(type(item))]
        except KeyError:
            raise TypeError("No instance for {}".format(item))


class TypeClass(object):
    __metaclass__ = TypeClassMeta

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
