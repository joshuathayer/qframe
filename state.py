import toolz.dicttoolz as d
import collections

class DB():

    def __init__(self, app, initial_val={}):
        self.app = app
        self.store = initial_val
        self.app.on_update(self.store)

    def get_in(self, ks):
        return(d.get_in(ks, self.store))

    def assoc_in(self, ks, val):
        self.store = d.assoc_in(self.store, ks, val)
        self.app.on_update(self.store)
        return(self.store)
