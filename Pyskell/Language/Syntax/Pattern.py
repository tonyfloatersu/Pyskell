def nt_to_tuple(nt):
    return tuple((getattr(nt, f) for f in nt.__class__._fields))
