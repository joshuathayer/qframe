from toolz.dicttoolz import get_in
from render import render
from components import component, REGISTERED_COMPONENTS
from subscriptions import subscribes
import state

app_state = {'items': [{'title': 'do a thing', 'body': 'do all the thing'},
                       {'title': 'go surf', 'body': 'ideally at bolinas'}],
             'headline': {'main': "to-do!",
                          'subheadline': "my to-do list"},
             'inbox': [{'id': 'm0', 'msg': 'item0'},
                       {'id': 'm1', 'msg': 'item1'},
                       {'id': 'm2', 'msg': 'item2'}]}

subscriptions = {'main-headline': ['headline', 'main'],
                 'sub-headline': ['headline', 'subheadline'],
                 'inbox': ['inbox']}

state.init_state(app_state)

@component
@subscribes(['inbox'], subscriptions)
def inbox(s):

    msgs = s['inbox']
    box = ['vbox/inbox-list', {}]

    for m in msgs:
        box.append(['label', {'id': m['id']}, m['msg']])

    return box

@component
@subscribes(['main-headline'], subscriptions)
def main_headline(s):

    headline = s['main-headline']
    return ['label/main_headline', {}, headline]

@component
def page():

    page = ['vbox/container',
             ['label/hello', "hello world from a vbox"],
             ['main_headline/headline'],
             ['inbox/inbox']]

    return page


res = render(page(), REGISTERED_COMPONENTS)

print(res)
