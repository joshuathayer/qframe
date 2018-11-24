from toolz.dicttoolz import get_in
import functools

COMPONENTS = {}


def render(component):
    print("Render! {}".format(component))
    res = None

    comp_name = component[0]
    comp_id = None
    if '/' in comp_name:
        (comp_name, comp_id) = component[0].split('/')

    if comp_id is None:
        if isinstance(component[1], dict) and 'id' in component[1]:
            comp_id = component[1]['id']

    if comp_id is None:
        raise ValueError("Components must have an ID")

    if comp_name in COMPONENTS:
        print("Woo it's wrapped")
        comp_fn = COMPONENTS[comp_name]
        res = render(comp_fn(*component[2:]))
        res['id'] = comp_id
    else:
        comp_args = component[1]
        comp_rest = component[2:]

        if comp_name in ['label','button']:
            res = {'component': comp_name,
                   'id': comp_id,
                   'text': comp_rest[0]}
        elif comp_name in ['vbox']:
            res = {'component': comp_name,
                   'id': comp_id,
                   'contains': list(map(render, comp_rest))}
        else:
            print("Dunno what that type is! {}".format(comp_type))

    return res


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


class component:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        COMPONENTS[self.func.__name__] = func

    def __call__(self, *args, **kwargs):
        print("Wrapped {}".format(self.func.__name__))
        return self.func(*args, **kwargs)

@component
def inbox():

    msgs = sub('inbox')
    box = ['vbox/inbox-list', {}]

    for m in msgs:
        box.append(['label', {'id': m['id']}, m['msg']])

    return box

@component
def main_headline():

    return ['label/main_headline', {}, sub('main-headline')]

@component
def page():

    page = ['vbox/container', {},
             ['label/hello', {}, "hello world from a vbox"],
             ['main_headline/headline', {}],
             ['inbox/inbox', {}]]
    return page


res = render(page())
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
