from typing import Type

def overrides(super_class: Type):
    def overrider(method):
        assert  method.__name__ in dir(super_class)
        return method
    
    return overrider