## like re-frame, but for python/qt

See layout.py for an example.

State is a dict

Subscriptions are paths into that dict

Components are functions which return vectors, where the first element is the name of a subcomponent (either a custom one, or an element defined by the library like 'label' or 'vbox).

Components are decorated by the `subscribes([...])` decorator, which declares the names of subscriptions the component requires (which are passed to the component function as keyword args).

The tree of components can be rendered to a single data structure which represents the UI of your application, and can be turned in to Qt UI with [reative-qt].

The magic happens when the `state` dict changes: the UI data structure is automatically rebuilt to reflect the new state of the DB. The react-qt project can efficiently re-reder the application UI based on changes in the rebuilt UI data structure.

So, *your application's user inferface is a function of your state dictionary* and *is reactive to changes in the dict*. Pretty neat.
