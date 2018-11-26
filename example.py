from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from reactive_qt.core import render_diff

import render
import layout

qapp = QApplication([])
window = QWidget()
vbox = QVBoxLayout()

class StatefulReactiveQtAppWindow(QWidget):
    def __init__(self, initial_layout=[], initial_elements={}):
        super().__init__()
        self.elements = initial_elements
        self.current_layout = initial_layout

    def next_layout(self, layout):
        print("NEXT LAYOUT!", layout)
        self.elements = render_diff(
            self.current_layout,
            layout,
            self.elements)

        self.current_layout = layout

appwindow = StatefulReactiveQtAppWindow({'id': 'container', 'contains': []},
                                        {'container': vbox})

layout.app.update_cb = lambda x: appwindow.next_layout(x)

appwindow.setLayout(vbox)
layout.state.init_state(layout.app_state, layout.app)
appwindow.show()
qapp.exec_()
