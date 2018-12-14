# These are actors which make up the logic of our application.

# In broad terms, this actor system should ingest events, and cause
# mutations in the database.

# All UI events route through this actor. In this case it's very
# simple- we just tell the DB actor about something to do.
class EventCatcher:
    def act(self, msg, tell, create):
        print("Event!", msg)
        event_key = msg[0]

        if event_key == 'input-changed':
            tell('updater', ['input', msg[1]])

        elif event_key == 'submit-clicked':
            tell('updater', ['submit'])

        elif type(event_key) == type(()):
            if event_key[0] == "todo-complete":
                completed = event_key[1]
                tell('updater', ['remove-todo', completed])

# All database mutations route through this actor
class DBUpdater:
    def __init__(self, db):
        self.db = db

    def act(self, msg, tell, create):
        msg_key = msg[0]

        if msg_key == 'input':
            self.db.assoc_in(['new-todo-text'], msg[1])

        elif msg_key == 'submit':
            todo_text = self.db.get_in(['new-todo-text'])
            todos = self.db.get_in(['todos'])

            new_todo_index = self.db.get_in(['todo-id'])

            todos.append({'id': str(new_todo_index),
                          'text': todo_text})

            self.db.assoc_in(['todos'], todos)
            self.db.assoc_in(['new-todo-text'], "")
            self.db.assoc_in(['todo-id'], new_todo_index + 1)

        elif msg_key == 'remove-todo':
            todos = self.db.get_in(['todos'])
            target_todo_id = msg[1]
            remaining_todos = list(filter(lambda t: t['id'] != target_todo_id, todos))
            self.db.assoc_in(['todos'], remaining_todos)
