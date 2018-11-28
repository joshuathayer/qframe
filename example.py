from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
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
    def __init__(self, initial_layout=[], initial_elements={}):
        super().__init__()
        self.elements = initial_elements
        self.current_layout = initial_layout

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

# when the local db updates and we have a new rendered UI description,
# tell the stateful UI handler about it
app.update_cb = lambda x: appwindow.next_layout(x)

# set Qt widget's initial layout (an empty vbox)
appwindow.setLayout(vbox)

# initialize db with state
db = state.DB(app, layout.app_state)

# create a tiny actor system: a timer which periodically pokes an
# updater, which sets the current time in the database
class Timer:
    def act(self, msg, tell, create):
        print("Timer")
        time.sleep(1)
        tell('updater','click')
        tell('timer','click')

class DBUpdater:
    def __init__(self, db):
        self.db = db

    def act(self, msg, tell, create):
        self.db.assoc_in(['time'], time.time())

system = spot.system.ActorSystem(qapp)
system.create_actor(Timer(), 'timer')
system.create_actor(DBUpdater(db), 'updater')

# kick off the actor network
system.tell('timer','click')

# show the UI
appwindow.show()
qapp.exec_()
