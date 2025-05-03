import os
from collections import namedtuple

# enter address & connection info for sending emails here

######################################################
details = {'senders_email': 'chalkuhns@gmail.com',
           'recipient_email': 'chalkuhns@gmail.com',
           'password': os.getenv('GM_PWD')}     # replace with app password from email account provider
                                                # if using gmail, create an app password here: https://myaccount.google.com/apppasswords
                                                # if using outlook, create an app password here: https://account.live.com/proofs/manage
                                                # if using yahoo, create an app password here: https://login.yahoo.com/account/security
######################################################


EmailInfo = namedtuple('EmailInfo', ['senders_email', 'recipient_email', 'password'])

email_info = EmailInfo(senders_email=details['senders_email'],
                  recipient_email=details['recipient_email'],
                  password=details['password'])