from toolz.dicttoolz import get_in
from render import render
from components import component, REGISTERED_COMPONENTS
from functools import wraps

state = {'items': [{'title': 'do a thing', 'body': 'do all the thing'},
                   {'title': 'go surf', 'body': 'ideally at bolinas'}],
         'headline': {'main': "to-do!",
                      'subheadline': "my to-do list"},
         'inbox': [{'id': 'm0', 'msg': 'item0'},
                   {'id': 'm1', 'msg': 'item1'},
                   {'id': 'm2', 'msg': 'item2'}]}

# we want to be able to subscribe components to parts of the state
# like

subscriptions = {'main-headline': ['headline', 'main'],
                 'sub-headline': ['headline', 'subheadline'],
                 'inbox': ['inbox']}

def sub(sub_name):
    path = subscriptions[sub_name]
    return get_in(path, state)

class subscribes:
    def __init__(self, subs):
        self.subs = subs

    def __call__(self, f):
        vals = {}

        for sub_name in self.subs:
            path = subscriptions[sub_name]
            vals[sub_name] = get_in(path, state)

        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(vals)

        return wrapped

@component
@subscribes(['inbox'])
def inbox(s):

    msgs = s['inbox']
    box = ['vbox/inbox-list', {}]

    for m in msgs:
        box.append(['label', {'id': m['id']}, m['msg']])

    return box

@component
def main_headline():

    return ['label/main_headline', {}, sub('main-headline')]

@component
def page():

    page = ['vbox/container',
             ['label/hello', {}, "hello world from a vbox"],
             ['main_headline/headline', {}],
             ['inbox/inbox', {}]]

    return page


res = render(page(), REGISTERED_COMPONENTS)

print(res)

# class StateNode:
#     def __init__(self, k, v):
#         self.k = k
#         self.v = v
#         self.subs = []
#         self.parent = None

# class AppState:
#     def __init__(self):
#         self.state = {}

#     def add_node(self, k, v):
#         self.state

#     def subscribe(self, path):



# #def item(item_path):


# def item_list(items):
#     return ['list-widget', items]

# def headline(text):
#     return "hello my headline is {}".format(text)

# def layout():
#     [headline 'headline']
