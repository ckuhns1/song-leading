import random as rd
from service.repository import Pool

class Song:
    def __init__(self, item):
        title, number = item.split(', ')
        self.title = title
        self.number = number

    def __repr__(self):
        return f'{self.number}, {self.title}\r\n'

class AMSongs:
    def __init__(self):
        pool = Pool()

        self.first = Song(rd.choice(pool.first))
        self.prayer = Song(rd.choice(pool.prayer))
        self.collection = Song(rd.choice(pool.collection))
        self.communion = Song(rd.choice(pool.communion))
        self.sermon = Song(rd.choice(pool.general))
        self.invitation = Song(rd.choice(pool.invitation))
    
    def export_for_email_am(self):
        self.songs = [self.first, self.prayer, self.collection, self.communion, self.sermon, self.invitation]
        return 'Sunday AM\r\n' + '\r\n' + self.songs.pop(0).__repr__() + self.songs.pop(0).__repr__() + \
            'OPENING PRAYER\r\n' + \
            self.songs.pop(0).__repr__() + '\r\nCOLLECTION\r\n' + \
            self.songs.pop(0).__repr__() + 'COMMUNION\r\n' + \
            self.songs.pop(0).__repr__() + '\r\nSCRIPTURE READING\\SERMON\r\n' + \
            self.songs.pop(0).__repr__()

class PMSongs:
    def __init__(self):
        pool = Pool()

        self.first = Song(rd.choice(pool.first))
        self.prayer = Song(rd.choice(pool.prayer))

        self.sermon = Song(rd.choice(pool.general))
        self.invitation = Song(rd.choice(pool.invitation))   
        self.communion = Song(rd.choice(pool.communion))
   
    def export_for_email_pm(self):
        self.songs = [self.first, self.prayer, self.sermon, self.invitation, self.communion]
        return 'Sunday PM\r\n' + '\r\n' + self.songs.pop(0).__repr__() + self.songs.pop(0).__repr__() + \
            'OPENING PRAYER\r\n' + \
            self.songs.pop(0).__repr__() + '\r\nSCRIPTURE READING\\SERMON\r\n' + \
            self.songs.pop(0).__repr__() + self.songs.pop(0).__repr__()

class WedsSongs:
    def export_for_email_weds(self):
        pass

class GospelMeetingSongs:
    def export_for_email_gospel_meeting(self):
        pass
