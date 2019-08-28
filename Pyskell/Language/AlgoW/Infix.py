class Infix:
    def __init__(self, f):
        self.f = f

    def __or__(self, other):
        return self.f(other)

    def __ror__(self, other):
        return Infix(lambda x: self.f(other, x))

    def __call__(self, v1, v2):
        return self.f(v1, v2)
