import toolz.dicttoolz

state = {}

def init_state(st):
    global state
    state = st

def get_in(path):
    global state
    return toolz.dicttoolz.get_in(path, state)
