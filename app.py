from render import render
from components import component, REGISTERED_COMPONENTS

top = None

def set_top(c):
    global top
    top = c

def on_update():
    print("DB updated. New UI")
    print(render(top(), REGISTERED_COMPONENTS))
