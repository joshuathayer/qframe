from components import component
from subscriptions import subscribes

app_state = {'items': [{'title': 'do a thing',
                        'body': 'do all the thing'},
                       {'title': 'go surf',
                        'body': 'ideally at bolinas'}],
             'headline': {'main': "to-do!",
                          'subheadline': "my to-do list"},
             'inbox': [{'id': 'm0', 'msg': 'item0'},
                       {'id': 'm1', 'msg': 'item1'},
                       {'id': 'm2', 'msg': 'item2'}],
             'time': 0}

subscriptions = {'main-headline': ['headline', 'main'],
                 'sub-headline': ['headline', 'subheadline'],
                 'inbox': ['inbox'],
                 'time': ['time']}

@component
@subscribes(['inbox'], subscriptions)
def inbox(subs):

    msgs = subs['inbox']
    box = ['vbox/inbox-list', {}]

    for m in msgs:
        box.append(['label', {'id': m['id']}, m['msg']])

    return box

@component
@subscribes(['main-headline'], subscriptions)
def main_headline(subs):

    headline = subs['main-headline']
    return ['label/main_headline', {}, headline]

@component
@subscribes(['time'], subscriptions)
def timer(subs):
    return ['label/currenttime', {}, str(subs['time'])]

@component
@subscribes([], subscriptions)
def page(subs):

    page = ['vbox/container',
            ['label/hello', {'text-color': 'blue'},
              "hello world from a vbox", {}],
            ['main_headline/headline', {}],
            ['timer/timer', {}],
            ['inbox/inbox', {}]]

    return page
