from qframe.components import component
from qframe.subscriptions import subscribes

from db import subscriptions

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
