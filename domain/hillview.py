from service.repository import Pool

class Song:
    def __init__(self, item):
        item = item + ['' for _ in range(6 - len(item))] # pad end of list with empty strings
        self.title, self.number = item[0], item[1]
        self.verses = item[2].split(' ')
        self.chorus_at_end = True if item[3] == '1' else False
        self.note = item[4]

    def __repr__(self):
        temp = ' '*(3-len(self.number)) + f'{self.number} {self.title}'
        if self.verses != ['']:
            temp += f' (Vss {", ".join(self.verses)})'
        if self.chorus_at_end:
            temp += ', CHORUS once at end only'
        return  temp + '\r\n'


class AMSongs:
    def __init__(self):
        self.pool = Pool()
        self.types = {'first': 'first',
                        'prayer': 'general',
                        'collection': 'general',
                        'communion': 'communion',
                        'sermon': 'general',
                        'invitation': 'invitation'}
        
        self.order = list(self.types.keys())

        for item in self.order:
            setattr(self, item, Song(self.pool.pick(getattr(self.pool, self.types[item]))))
    
        self.songs = [self.first, self.prayer, self.collection, self.communion, self.sermon, self.invitation]
    
    def export_for_email(self):
        return 'Sunday AM\r\n' + '\r\n' + \
            self.first.__repr__() + \
            self.prayer.__repr__() + '\r\n'\
            '  OPENING PRAYER\r\n' + \
            self.collection.__repr__() + '\r\n' + \
            '  COLLECTION\r\n' + \
            self.communion.__repr__() + '\r\n' +\
            '  COMMUNION\r\n' + \
            self.sermon.__repr__() + '\r\n' +\
            '  SCRIPTURE READING\\SERMON\r\n' + \
            self.invitation.__repr__()
    
    def export_for_revision(self):
        nbr_songs = len(self.songs)
        nbrs = [str(i) for i in range(1, nbr_songs + 1)]

        print('Sunday AM\r\n' + '\r\n' + \
            f'({nbrs.pop(0)})  ' + self.first.__repr__() + \
            f'({nbrs.pop(0)})  ' + self.prayer.__repr__() + \
            '     OPENING PRAYER\r\n' + \
            f'({nbrs.pop(0)})  ' + self.collection.__repr__() + \
            '     COLLECTION\r\n' + \
            f'({nbrs.pop(0)})  ' + self.communion.__repr__() + \
            '     COMMUNION\r\n' + \
            f'({nbrs.pop(0)})  ' + self.sermon.__repr__() + \
            '     SCRIPTURE READING\\SERMON\r\n' + \
            f'({nbrs.pop(0)})  ' + self.invitation.__repr__() )


class PMSongs:
    def __init__(self):
        self.pool = Pool()
        self.types = {'first': 'general',
                      'prayer': 'general',
                      'sermon': 'general',
                      'invitation': 'invitation',
                      'communion': 'communion'}
        
        self.order = list(self.types.keys())

        for item in self.order:
            setattr(self, item, Song(self.pool.pick(getattr(self.pool, self.types[item]))))

        self.songs = [self.first, self.prayer, self.sermon, self.invitation, self.communion]
    
    def export_for_email(self):
        return 'Sunday PM\r\n' + '\r\n' + \
            self.first.__repr__() + \
            self.prayer.__repr__() + '\r\n' +\
            '  OPENING PRAYER\r\n' + \
            self.sermon.__repr__() + '\r\n' +\
            '  SCRIPTURE READING\\SERMON\r\n' + \
            self.invitation.__repr__() + \
            self.communion.__repr__()
    
    def export_for_revision(self):
        nbr_songs = len(self.songs)
        nbrs = [str(i) for i in range(1, nbr_songs + 1)]

        print('Sunday PM\r\n' + '\r\n' + \
            f'({nbrs.pop(0)})  ' + self.first.__repr__() + \
            f'({nbrs.pop(0)})  ' + self.prayer.__repr__() + \
            '     OPENING PRAYER\r\n' + \
            f'({nbrs.pop(0)})  ' + self.sermon.__repr__() + \
            '     SCRIPTURE READING\\SERMON\r\n' + \
            f'({nbrs.pop(0)})  ' + self.invitation.__repr__() + \
            f'({nbrs.pop(0)})  ' + self.communion.__repr__() )


class WedsSongs:
    def __init__(self):
        pass

    def export_for_email(self):
        pass


class GospelMeetingSongs:
    def __init__(self):
        pass

    def export_for_email(self):
        pass


class BaptismSongs:
    def __init__(self):
        pass

    def export_for_email(self):
        pass