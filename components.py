import functools

REGISTERED_COMPONENTS = {}

class component:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        REGISTERED_COMPONENTS[self.func.__name__] = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
