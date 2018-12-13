from toolz.dicttoolz import get_in
from functools import wraps

class subscribes:
    def __init__(self, subs, all_subscriptions):
        self.all_subscriptions = all_subscriptions
        self.subs = subs

    def __call__(self, f):

        vals = {}

        @wraps(f)
        def wrapped(state, *args, **kwargs):
            for sub_name in self.subs:
                path = self.all_subscriptions[sub_name]
                vals[sub_name] = get_in(path, state)

            return f(vals)

        return wrapped
