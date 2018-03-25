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
        if isinstance(p_t1.name, TypeVariable) and len(p_t1.types) > 0:
            p_t1.name = p_t2.name
            p_t1.types = p_t2.types
            unify_types(p_t1, p_t2)
        elif isinstance(p_t2.name, TypeVariable):
            unify_types(p_t2, p_t1)
        elif p_t1.name != p_t2.name or len(p_t1.types) != len(p_t2.types):
            raise TypeError("Type mismatch: {0} != {1}".format(str(p_t1),
                                                               str(p_t2)))
        for p, q in zip(p_t1.types, p_t2.types):
            unify_types(p, q)
    else:
        raise InferenceError("Unify_types: something cannot be unified")


def fresh(t, non_generic):
    map_to = {}

    def fresh_closure(tp):
        p = prune(tp)
        if isinstance(p, TypeVariable):
            if is_generic(p, non_generic):
                if p not in map_to:
                    map_to[p] = TypeVariable()
                return map_to[p]
            else:
                return p
        elif isinstance(p, TypeOperator):
            return TypeOperator(p.name, [fresh_closure(i) for i in p.types])
    return fresh_closure(t)


def get_type(name, env, non_generic):
    if name in env:
        return fresh(env[name], non_generic)
    raise InferenceError("Undefined symbol: {}".format(name))


def analyze(node, env, non_generic=None):
    """
    Computes the type of the expression `node`.
    :param node: The root of the AST/ABT
    :param env: The type env mapping expr-identifier-names to type assignments
    :param non_generic: A set of non-generic variables
    :return: The computed type of the expression
    """
    if non_generic is None:
        non_generic = set()
    if isinstance(node, Variable):
        return get_type(node.name, env, non_generic)
    elif isinstance(node, FunctionApplication):
        fun_type = analyze(node.func, env, non_generic)
        arg_type = analyze(node.args, env, non_generic)
        res_type = TypeVariable()
        unify_types(Function(arg_type, fun_type), res_type)
        return res_type
    elif isinstance(node, Lambda):
        arg_type = TypeVariable()
        new_env = env.copy()
        new_env[node.args] = arg_type
        new_non_generic = non_generic.copy()
        new_non_generic.add(node.args)
        res_type = analyze(node.exec_body, new_env, new_non_generic)
        return Function(arg_type, res_type)
    elif isinstance(node, Let):
        new_type = TypeVariable()
        new_env = env.copy()
        new_env[node.expr] = new_type
        new_non_generic = non_generic.copy()
        new_non_generic.add(new_type)
        rep_type = analyze(node.rep, new_env, new_non_generic)
        unify_types(rep_type, new_type)
        return analyze(node.env_expr, new_env, new_non_generic)
    else:
        assert False, "Unrecognized syntax string: {}".format(str(node))
