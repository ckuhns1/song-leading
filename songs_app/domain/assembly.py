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
        return  '  ' + temp + '\r\n'


class Service:
    def __init__(self, song_design, event_design):
        self.pool = Pool()
        self.events = event_design
        self.types = song_design
        
        self.order = list(self.types.keys()) # used in driver flow
        
        for item in self.types:
            setattr(self, item, Song(self.pool.pick_new_song_remove(getattr(self.pool, self.types[item]))))

    @property    # enables updates to individual songs to be reflected in Service.songs list
    def songs(self):
        return [getattr(self, item) for item in self.order]
        
    def export_for_email(self):
        temp = ''
        song_iter = iter(self.songs)

        for item in self.events.values():
            temp += item[0] + '\r\n'
            for _ in range(item[1]):
                temp += next(song_iter).__repr__()
        return temp
    
    def export_for_revision(self):
        temp = ''
        nbr = 0
        for item in self.events.values():
            temp += item[0] + '\r\n'
            for _ in range(item[1]):
                temp += f'({str(nbr+1)})' + self.songs[nbr].__repr__()
                nbr += 1
        print(temp)



