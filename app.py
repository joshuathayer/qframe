from render import render
from components import component, REGISTERED_COMPONENTS

class App:
    def __init__(self, update_cb = None, event_cb = None):
        self.top = None

        # what to do when the db updates
        self.update_cb = update_cb

        # what to do when there's an outside action
        self.event_cb = event_cb

    def set_top(self, c):
        self.top = c

    def on_update(self, db):
        new_layout = render(self.top(db),
                            self.event_cb,
                            [REGISTERED_COMPONENTS, db])

        if self.update_cb is not None:
            self.update_cb(new_layout)
