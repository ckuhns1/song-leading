import os

# enter service design here
#################################################
'''
The Sunday AM & PM service layouts for Hillview Terrace church of Christ are below, and serve
as a template for others. To add new layouts:

    1. Create a dictionary for the morning service with keys for each position and values 
        as the song grouping, matching the categories in infra/.

    2. Create a dictionary for the morning service with keys for each event and values as 
        a list containing the event description and the number of songs before the next event.

        E.g. {'communion': ['Lord's Supper:', 2]} specifies the Lord's Supper (situated between songs),
        and there are 2 songs before the next event.

    3. Repeat steps 1 and 2 for the evening service.

    4. Create a class with the name of the church, following the example below.

    5. Add the class to the list of service layouts in master.py. (Alternatively, modify the existing 
        class to suit the new layout.)
'''


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
######################################################




# enter address & connection info for sending emails here
######################################################
contact_details = {'senders_email': 'make.melody.eph519@gmail.com',
           'recipient_email': 'chalkuhns@gmail.com',
           'password': os.getenv('GM_PWD')}     # replace with app password from email account provider
                                                # if using gmail, create an app password here: https://myaccount.google.com/apppasswords
                                                # if using outlook, create an app password here: https://account.live.com/proofs/manage
                                                # if using yahoo, create an app password here: https://login.yahoo.com/account/security
######################################################

class Hillview:
    def __init__(self):
        self.am_songs = am_songs_hillview
        self.pm_songs = pm_songs_hillview
        self.am_events = am_events_hillview
        self.pm_events = pm_events_hillview
        self.email_info = contact_details