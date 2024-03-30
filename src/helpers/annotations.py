from typing import Type


def overrides(super_class: Type):
    def overrider(method):
        assert(method.__name__ in dir(super_class))
        method.__doc__ = dir(super_class)[method.__name__].__doc__
        return method
    
    return overrider