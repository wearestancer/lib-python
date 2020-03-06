# -*- coding: utf-8 -*-


def add_constant(*args):
    """
    Add constants to a class.
    """

    def wrapper(cls):
        class Constant(cls):
            def __getattr__(self, attr):
                cst = attr.lower()

                if cst in args:
                    return cst

                if hasattr(super(), '__getattr__') and callable(getattr(super(), '__getattr__')):
                    return super().__getattr__(self, attr)

                raise AttributeError

            def __setattr__(self, attr, value):
                raise SyntaxError('You can not modify a constant ({})'.format(attr.upper()))

        tmp = [''] + [a.upper() for a in args]
        Constant.__doc__ = cls.__doc__ + '\n\nConstants available:' + '\n  - '.join(tmp)

        return Constant
    return wrapper
