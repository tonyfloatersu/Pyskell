from HMTypeSystem import *
from PyskellTypeSystem import *


def _t(obj):
    return str(type_of(obj))


def _q(quit_status=None):
    if quit_status is None:
        quit()
    else:
        quit(quit_status)
