import toolz.dicttoolz
import collections

class DB(collections.MutableMapping):

    def __init__(self, app, initial_val={}):
        self.app = app
        self.store = initial_val
        self.app.on_update(self.store)

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value
        self.app.on_update(self.store)

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

# state = {}

# I really don't like that we pass app into these.

# def init_state(st, app):
#     global state
#     state = st
#     app.on_update()

# def get_in(path):
#     global state
#     return toolz.dicttoolz.get_in(path, state)

# def assoc_in(path, val, app):
#     global state
#     state = toolz.dicttoolz.assoc_in(state, path, val)
#     app.on_update()

# def update_in(path, f, app):
#     global state
#     state = toolz.dicttoolz.update_in(state, path, f)
#     app.on_update()
