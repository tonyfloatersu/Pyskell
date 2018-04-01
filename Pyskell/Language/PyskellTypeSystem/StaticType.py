"""
Oh... Chill, don't get static
"""
from Pyskell.Language.HMTypeSystem import *


class BaseType(object):
    def __type__(self):
        return TypeError("Touch base")


class Undefined(BaseType):
    def __type__(self):
        return TypeVariable()
