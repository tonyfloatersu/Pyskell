from TypeComponent import *


def prune(tp):
    """
    Side effect function, collapses the list of type instances.
    Returns currently defining instance of type `tp`
    :param tp: TypeOperator or TypeVariable
    :return the type expression:
    - TypeOperator
    - Un-instanced Type Variable
    """
    if isinstance(tp, TypeVariable):
        if tp.instance is not None:
            tp.instance = prune(tp.instance)
            return tp.instance
    return tp


def occur_in_type(tp, target_type):
    """
    Find `tp` if it is in `target_type`.
    WARNING: `tp` MUST BE PRE-PRUNED OR JUST HAVE-NO-INSTANCE
    By pruning the `target_type` we can get 2 situations:
    - `target_type` is pruned to un-instance situation, just compare
    - `target_type` is TypeOperator, so lookup in the types
    Finally, return T/F
    """
    pruned_type = prune(target_type)
    if tp == pruned_type:
        return True
    elif isinstance(pruned_type, TypeOperator):
        return occur_in(tp, pruned_type.types)
    return False


def occur_in(tp, types):
    """
    Find `tp` among all the `types` by calling `occur_in_type`.
    """
    return any(map(lambda x: occur_in_type(x, tp), types))


def unify_to_type(tp_var, tp):
    pass


def unify_types(type1, type2):
    pass
