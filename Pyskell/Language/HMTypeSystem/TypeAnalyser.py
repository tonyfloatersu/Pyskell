from TypeComponent import *
from SyntaxComponent import *


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


def unify_type(tp_1, tp_2):
    def bind(t_1, t_2):
        if t_1 != t_2:
            if isinstance(t_2, TypeVariable):
                union = tuple(set(t_1.constraints + t_2.constraints))
                t_1.constraints = union
                t_2.constraints = union
            if occur_in_type(t_1, t_2):
                raise InferenceError("Recursive Type Infinite")
            t_1.instance = t_2

    def unify_type_operator(to_1, to_2):
        # poly
        if isinstance(to_1.name, TypeVariable) and len(to_1.types) > 0:
            to_1.name = to_2.name
            to_1.types = to_2.types
            unify_type(to_1, to_2)
        elif isinstance(to_2.name, TypeVariable):
            unify_type(to_2, to_1)
        # mono
        elif to_1.name != to_2.name or len(to_1.types) != len(to_2.types):
            raise InferenceError("Unify Mismatch: {} != {}".format(to_1, to_2))
        for i, j in zip(to_1.types, to_2.types):
            unify_type(i, j)

    type_1, type_2 = prune(tp_1), prune(tp_2)
    if isinstance(type_1, TypeOperator) and isinstance(type_2, TypeOperator):
        unify_type_operator(type_1, type_2)
    elif isinstance(type_1, TypeVariable):
        bind(type_1, type_2)
    elif isinstance(type_2, TypeVariable):
        bind(type_2, type_1)
    else:
        assert False, "Unify Type fail: {0}, {1}".format(type_1, type_2)


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
    elif isinstance(node, FuncApp):
        fun_type = analyze(node.expr_func, env, non_generic)
        arg_type = analyze(node.expr_arg, env, non_generic)
        res_type = TypeVariable()
        unify_type(Arrow(arg_type, res_type), fun_type)
        return res_type
    elif isinstance(node, Lambda):
        arg_type = TypeVariable()
        new_env = env.copy()
        new_env[node.name] = arg_type
        new_non_generic = non_generic.copy()
        new_non_generic.add(arg_type)
        res_type = analyze(node.expr_body, new_env, new_non_generic)
        return Arrow(arg_type, res_type)
    elif isinstance(node, Let):
        new_type = TypeVariable()
        new_env = env.copy()
        new_env[node.name_replaced] = new_type
        new_non_generic = non_generic.copy()
        new_non_generic.add(new_type)
        rep_type = analyze(node.expr_replacement, new_env, new_non_generic)
        unify_type(new_type, rep_type)
        return analyze(node.expr, new_env, new_non_generic)
    else:
        assert False, "Unrecognized syntax string: {}".format(str(node))
