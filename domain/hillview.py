import random as rd
from service.repository import Pool

class Song:
    def __init__(self, item):
        item = item + ['' for _ in range(6 - len(item))]
        self.title, self.number = item.pop(0), item.pop(0)
        self.verses = item.pop(0).split(' ')
        self.chorus_at_end = True if item.pop(0) == '1' else False
        self.note = item.pop(0)

    @staticmethod
    def pick(group):
        song = rd.choice(group)
        group.remove(song)
        return Song(song)

    def __repr__(self):
        temp = f'{self.number} {self.title}'
        if self.verses != ['']:
            temp += f' (Vss {", ".join(self.verses)})'
        if self.chorus_at_end:
            temp += ', CHORUS once at end only'
        return  temp + '\r\n'

class AMSongs:
    def __init__(self):
        pool = Pool()

        self.first = Song.pick(pool.first)
        self.prayer = Song.pick(pool.general)
        self.collection = Song.pick(pool.general)
        
        self.communion = Song.pick(pool.communion)
        self.sermon = Song.pick(pool.general)
        self.invitation = Song.pick(pool.invitation)
    

    
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

        self.first = Song.pick(pool.general)
        self.prayer = Song.pick(pool.general)

        self.sermon = Song.pick(pool.general)
        self.invitation = Song.pick(pool.invitation)
        self.communion = Song.pick(pool.communion)


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
