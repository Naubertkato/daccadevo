def set_module(module):
    """Private decorator for overriding __module__ on a function or class.

    Inspired by usage in libraries such as Numpy and Pandas

    """

    def decorator(func):
        if module is not None:
            func.__module__ = module
        return func

    return decorator
