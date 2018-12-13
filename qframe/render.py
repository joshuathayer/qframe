from toolz.functoolz import partial, flip, memoize

@memoize(key=lambda args, kwargs: args[0])
def make_event_cb(event_key, event_cb):
    return lambda x: event_cb([event_key, x])

def render(component, event_cb, state):
    [components, db] = state
    res = None

    comp_name = component[0]
    comp_id = None
    if '/' in comp_name:
        (comp_name, comp_id) = component[0].split('/')

    if comp_id is None:
        if isinstance(component[1], dict) and 'id' in component[1]:
            comp_id = component[1]['id']

    if comp_id is None:
        raise ValueError("Components must have an ID")

    if comp_name in components:
        comp_fn = components[comp_name]
        comp_res = comp_fn(db, *component[2:])
        res = render(comp_res, event_cb, [components, db])
        res['id'] = comp_id
    else:
        if isinstance(component[1], dict):
            comp_args = component[1]
            comp_rest = component[2:]
        else:
            comp_args = {}
            comp_rest = component[1:]

        if comp_name in ['label']:
            res = {'component': comp_name,
                   'id': comp_id,
                   'text': comp_rest[0]}
        elif comp_name in ['pushbutton']:
            res = {'component': comp_name,
                   'id': comp_id,
                   'text': comp_rest[0]}
            if 'on-click' in comp_args:
                res['on-click'] = make_event_cb(comp_args['on-click'],
                                                event_cb)
        elif comp_name in ['lineedit']:
            res = {'component': comp_name,
                   'id': comp_id,
                   'text': comp_rest[0]}
            if 'on-edit' in comp_args:
                res['on-edit'] = make_event_cb(comp_args['on-edit'],
                                               event_cb)
        elif comp_name in ['vbox', 'hbox']:
            res = {'component': comp_name,
                   'id': comp_id,
                   'contains': list(
                       map(lambda comp: render(comp,
                                               event_cb,
                                               [components, db]),
                           comp_rest))}
        else:
            print("Dunno what that type is! {}".format(comp_name))

    return res
