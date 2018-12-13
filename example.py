from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject
from reactive_qt.core import render_diff

import render
import layout

import app
import state

import spot.system
from datetime import datetime
import time

# out qframe app, just holds on to the root of our component tree, and
# provides a callback for the db when it changes.
app = app.App()
app.set_top(layout.page)

# Qt boilerplate for app initialization
qapp = QApplication([])
window = QWidget()

# this will be the element that'll hold our entire UI
vbox = QVBoxLayout()

# this should go into reactive-qt. it's a simple handler for managing
# the call to reactive_qt.render_diff() (basically, it just keeps the
# current layout in state, since the call to render_diff is stateless)
class StatefulReactiveQtAppWindow(QWidget):

    # A signal to hit when the layout changes, so we can be sure to
    # run the layout mutations in the UI thread
    layout_changed = pyqtSignal(object)

    def __init__(self, initial_layout=[], initial_elements={}):
        super().__init__()
        self.elements = initial_elements
        self.current_layout = initial_layout
        self.layout_changed.connect(self.next_layout)

    @pyqtSlot(object)
    def next_layout(self, layout):
        self.elements = render_diff(
            self.current_layout,
            layout,
            self.elements)

        self.current_layout = layout

# initialize our stateful UI handler with the current UI and the dict
# of element IDs to Qt object (both just hold the empty container
# element)
appwindow = StatefulReactiveQtAppWindow({'id': 'container',
                                         'contains': []},
                                        {'container': vbox})

# When the local db updates and we have a new rendered UI description,
# tell the stateful UI handler about it.
#
# This callback ends up getting run in an arbitrary thread. We don't
# want that: we want it to run in the UI thread, at least the bits
# which may make new Qt bits. We use Qt's signals and slots to
# facilitate this.
app.update_cb = lambda x: appwindow.layout_changed.emit(x)

# set Qt widget's initial layout (an empty vbox)
appwindow.setLayout(vbox)

# We're going to define the logic of our application in a small actor
# system.
system = spot.system.ActorSystem(qapp)

# And tell our application what to do when any UI action happens:
# place it in the `event` actor
app.event_cb = lambda event: system.tell('event', event)

# initialize db with state
db = state.DB(app, layout.app_state)

# Define out tiny actor system: a timer which periodically pokes an
# updater, which sets the current time in the database
class Timer:
    def act(self, msg, tell, create):
        time.sleep(1)
        tell('updater', ['tick'])
        tell('timer','tick')

class DBUpdater:
    def __init__(self, db):
        self.db = db

    def act(self, msg, tell, create):

        msg_key = msg[0]

        if msg_key == 'tick':
            self.db.assoc_in(['time'], time.time())
        elif msg_key == 'input':
            self.db.assoc_in(['incoming_text'], msg[1])
        elif msg_key == 'submit':
            text = self.db.get_in(['incoming_text'])
            inbox = self.db.get_in(['inbox'])
            index = len(inbox)
            inbox.append({'id': "m" + str(index), 'msg': text})
            self.db.assoc_in(['inbox'], inbox)
            self.db.assoc_in(['incoming_text'], "")

class EventCatcher:
    def act(self, msg, tell, create):
        print("Got an _event_!", msg)
        event_key = msg[0]

        if event_key == 'input-changed':
            tell('updater', ['input', msg[1]])
        elif event_key == 'submit-clicked':
            tell('updater', ['submit'])

system.create_actor(Timer(), 'timer')
system.create_actor(DBUpdater(db), 'updater')
system.create_actor(EventCatcher(), 'event')

# kick off the actor network
system.tell('timer','click')

# show the UI
appwindow.show()
qapp.exec_()
