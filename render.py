from toolz.functoolz import partial, flip

def render(component, components):
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
        comp_res = comp_fn(*component[2:])
        res = render(comp_res, components)
        res['id'] = comp_id
    else:
        if isinstance(component[1], dict):
            comp_args = component[1]
            comp_rest = component[2:]
        else:
            comp_args = {}
            comp_rest = component[1:]

        if comp_name in ['label','button']:
            res = {'component': comp_name,
                   'id': comp_id,
                   'text': comp_rest[0]}
        elif comp_name in ['vbox']:
            res = {'component': comp_name,
                   'id': comp_id,
                   'contains': list(
                       map(partial(flip(render), components),
                           comp_rest))}
        else:
            print("Dunno what that type is! {}".format(comp_name))

    return res
