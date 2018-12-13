# an initial database. this is just data.
app_state = {'items': [{'title': 'do a thing',
                        'body': 'do all the thing'},
                       {'title': 'go surf',
                        'body': 'ideally at bolinas'}],
             'headline': {'main': "to-do!",
                          'subheadline': "my to-do list"},
             'inbox': [{'id': 'm0', 'msg': 'item0'},
                       {'id': 'm1', 'msg': 'item1'},
                       {'id': 'm2', 'msg': 'item2'}],
             'incoming_text': "",
             'time': 0}

# a map of names to paths into the database. our components can
# subscribe to these, and when data at those paths change, the
# components will be redrawn.
subscriptions = {'main-headline': ['headline', 'main'],
                 'sub-headline': ['headline', 'subheadline'],
                 'inbox': ['inbox'],
                 'time': ['time'],
                 'incoming_text': ['incoming_text']}
