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

app = app.App()

qapp = QApplication([])
window = QWidget()
vbox = QVBoxLayout()


app.set_top(layout.page)



# this should go into reactive-qt
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

appwindow = StatefulReactiveQtAppWindow({'id': 'container',
                                         'contains': []},
                                        {'container': vbox})

app.update_cb = lambda x: appwindow.next_layout(x)

appwindow.setLayout(vbox)

# initialize db with state
db = state.DB(app, layout.app_state)



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
system.tell('timer','click')

# simulate updating db
db.assoc_in(['headline','main'], "These are my TODOs")

appwindow.show()
qapp.exec_()
