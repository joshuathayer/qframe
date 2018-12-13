import time

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
