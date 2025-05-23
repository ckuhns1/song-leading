from service.repository import Pool
import streamlit as st

class Song:
    def __init__(self, item):
        item = item + ['' for _ in range(6 - len(item))] # pad end of list with empty strings
        self.title, self.number = item[0].title(), item[1]
        self.verses = item[2].split(' ')
        self.chorus_at_end = True if item[3] == '1' else False
        self.note = item[4]

    def __repr__(self):
        pad_length = 3 - len(self.number)
        temp = f" **{self.number} -- {self.title}**"

        if self.verses != ['']:
            temp += f"   (_Verses: {', '.join(self.verses)}_)"

        if self.chorus_at_end:
            temp += "   (((_Chorus at end only_)))"

        return temp + "  \n"






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
            temp += f"\n## {item[0]}\n\n"
            temp += "---\r\n" if nbr == 0 else ""   # Section header with blank lines around
            for _ in range(item[1]):
                ref = f"**`({nbr + 1})`**"   # Reference number bold with backticks
                temp += f"{ref} {self.songs[nbr].__repr__()}\n"
                nbr += 1
        return temp

    def has_duplicates(self):
        return not len({song.number for song in self.songs}) == len(self.types)
    
    def search_pool(self, song_nbr, search_str):
        song_to_change = self.order[song_nbr - 1]
        pool = getattr(self.pool, self.types[song_to_change])

        if search_str.isdigit():
            matches = [s for s in pool if search_str == s[1]]
        else:
            matches = [s for s in pool if search_str in s[0].lower()]
        if not matches:
            st.text("No matches\r\n"*3)
        
        return matches

