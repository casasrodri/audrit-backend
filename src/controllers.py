class StaticMethodsMeta(type):
    def __new__(cls, name, bases, dct):
        for key, value in dct.items():
            if callable(value):
                dct[key] = staticmethod(value)
        return super(StaticMethodsMeta, cls).__new__(cls, name, bases, dct)


class BaseController(metaclass=StaticMethodsMeta):
    ...
