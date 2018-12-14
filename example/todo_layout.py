from qframe.components import component
from qframe.subscriptions import subscribes

from todo_db import subscriptions

def todo(id, text):
    return ['hbox', {'id': "todo-container-" + str(id)},
            ['label', {'id': "todo-text-" + str(id)}, text],
            ['pushbutton', {'id': "todo-complete-" + str(id),
                            'on-click': ("todo-complete", str(id))},
             "Done"]]

@component
@subscribes(['todos'], subscriptions)
def todo_list(subs):
    todos = subs['todos']
    todo_container = ['vbox/todo-list', {}]

    for t in todos:
        todo_container.append(todo(t['id'], t['text']))

    return todo_container

@component
@subscribes(['new-todo-text'], subscriptions)
def todo_input(subs):
    return ['lineedit/todoinput',
            {'on-edit': 'input-changed'},
            str(subs['new-todo-text'])]

@component
@subscribes([], subscriptions)
def todo_app(subs):
    return ['vbox/container',
            ['label/headline', {}, "Todos"],
            ['todo_list/todos', {}],
            ['hbox/todobox', {},
             ['todo_input/todo-input'],
             ['pushbutton/todo-submit',
              {'on-click': 'submit-clicked'},
              "Submit"]]]
