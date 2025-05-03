am_songs_hillview = {'first': 'first', # position name: song group (see infra directory)
                        'prayer': 'general',
                        'collection': 'general',
                        'communion': 'communion',
                        'sermon': 'general',
                        'invitation': 'invitation'}

am_events_hillview = {'name': ['Sunday AM:', 2], # number in value is number of songs until next event
                         'o_prayer': ['OPENING PRAYER', 1],
                         'collection': ['COLLECTION', 1],
                         'communion': ['COMMUNION', 1],
                         'sermon': ['SCRIPTURE READING\\SERMON', 1],
                         'c_prayer': ['CLOSING PRAYER', 0]}

pm_songs_hillview = {'first': 'general',
                      'prayer': 'general',
                      'sermon': 'general',
                      'invitation': 'invitation',
                      'communion': 'communion'}

pm_events_hillview = {'name': ['Sunday PM:', 2],
                            'o_prayer': ['OPENING PRAYER', 1],
                            'sermon': ['SCRIPTURE READING\\SERMON', 2],
                            'c_prayer': ['CLOSING PRAYER', 0]}



class Hillview:
    def __init__(self):
        self.am_songs = am_songs_hillview
        self.pm_songs = pm_songs_hillview
        self.am_events = am_events_hillview
        self.pm_events = pm_events_hillview