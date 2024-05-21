from typing import Type

def overrides(super_class: Type):
    """annotates a class method and specifies that is should be an override of a method from the specified base class

    Args:
        super_class (Type): the base class this class inherits
    """
    def overrider(method):
        assert  method.__name__ in dir(super_class)
        return method
    
    return overrider