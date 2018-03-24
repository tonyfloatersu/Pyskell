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


def is_generic(tp, not_generic):
    return not occur_in(tp, not_generic)


def unify_types(type1, type2):
    def unify_with_type_variable(type_var, type_unknown):
        if type_var != type_unknown:
            if occur_in_type(type_var, type_unknown):
                raise InferenceError("Unify_types: recursive unify error")
            union = tuple(set(type_var.constraints + type_unknown.constraints))
            type_var.constraints = union
            type_unknown.constraints = union
            type_var.instance = type_unknown
    p_t1 = prune(type1)
    p_t2 = prune(type2)
    if isinstance(p_t1, TypeVariable):
        unify_with_type_variable(p_t1, p_t2)
    elif isinstance(p_t1, TypeOperator) and isinstance(p_t2, TypeVariable):
        unify_with_type_variable(p_t2, p_t1)
    elif isinstance(p_t1, TypeOperator) and isinstance(p_t2, TypeOperator):
        pass
    else:
        raise InferenceError("Unify_types: something cannot be unified")
