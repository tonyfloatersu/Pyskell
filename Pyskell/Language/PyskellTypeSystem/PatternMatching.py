from AlgebraicDataType import ADT


def nt_to_tuple(nt):
    return tuple((getattr(nt, f) for f in nt.__class__._fields))


class PatternMatchBind(object):
    def __init__(self, name):
        self.name = name


class PatternMatchListBind(object):
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail


def pattern_match(value, pattern, env=None):
    env = {} if env is None else env
    if isinstance(pattern, PatternMatchBind):
        if pattern.name in env:
            raise SyntaxError("Conflicting definitions: {}" % pattern.name)
        env[pattern.name] = value
        return True, env

    elif isinstance(pattern, PatternMatchListBind):
        head, tail = list(value[:len(pattern.head)]), value[len(pattern.head):]
        matches, env = pattern_match(head, pattern.head, env)
        if matches:
            return pattern_match(tail, pattern.tail, env)
        return False, env

    elif type(value) == type(pattern):
        if isinstance(value, ADT):
            return pattern_match(nt_to_tuple(value), nt_to_tuple(pattern), env)

        elif hasattr(value, "__iter__"):
            matches = []
            if len(value) != len(pattern):
                return False, env

            for v, p in zip(value, pattern):
                match_status, env = pattern_match(v, p, env)
                matches.append(match_status)
            return all(matches), env

        elif value == pattern:
            return True, env

    return False, env
