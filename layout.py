from components import component
from subscriptions import subscribes

# an initial database. this is just data.
app_state = {'items': [{'title': 'do a thing',
                        'body': 'do all the thing'},
                       {'title': 'go surf',
                        'body': 'ideally at bolinas'}],
             'headline': {'main': "to-do!",
                          'subheadline': "my to-do list"},
             'inbox': [{'id': 'm0', 'msg': 'item0'},
                       {'id': 'm1', 'msg': 'item1'},
                       {'id': 'm2', 'msg': 'item2'}],
             'incoming_text': "",
             'time': 0}

# a map of names to paths into the database. our components can
# subscribe to these, and when data at those paths change, the
# components will be redrawn.
subscriptions = {'main-headline': ['headline', 'main'],
                 'sub-headline': ['headline', 'subheadline'],
                 'inbox': ['inbox'],
                 'time': ['time'],
                 'incoming_text': ['incoming_text']}

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
@subscribes(['incoming_text'], subscriptions)
def text_input(subs):
    return ['lineedit/todoinput',
            {'on-edit': 'input-changed'},
            str(subs['incoming_text'])]

@component
@subscribes([], subscriptions)
def page(subs):

    page = ['vbox/container',
            ['label/hello', {'text-color': 'blue'},
              "hello world from a vbox", {}],
            ['main_headline/headline', {}],
            ['inbox/inbox', {}],
            ['timer/timer', {}],
            ['hbox/inputbox', {},
             ['text_input/text_input'],
             ['pushbutton/todosubmit',
              {'on-click': 'submit-clicked'},
              "Submit"]
            ],
    ]

    return page
