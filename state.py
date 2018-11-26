import toolz.dicttoolz
# import app

state = {}

def init_state(st, app):
    global state
    state = st
    app.on_update()

def get_in(path):
    global state
    return toolz.dicttoolz.get_in(path, state)

def assoc_in(path, val, app):
    global state
    state = toolz.dicttoolz.assoc_in(state, path, val)
    app.on_update()

def update_in(path, f, app):
    global state
    state = toolz.dicttoolz.update_in(state, path, f)
    app.on_update()
