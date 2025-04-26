class Song:
    def __init__(self, item):
        title, number = item.split(', ')
        self.title = title
        self.number = number

    def __repr__(self):
        return f'{self.number}, {self.title}\r\n'

class HtSongs:
    def __init__(self, date):
        self.date = date
        self.songs = []
    
    def export_for_email_am(self):
        return 'Sunday AM\r\n' + '\r\n' + self.songs.pop(0).__repr__() + self.songs.pop(0).__repr__() + \
            'OPENING PRAYER\r\n' + \
            self.songs.pop(0).__repr__() + '\r\nCOLLECTION\r\n' + \
            self.songs.pop(0).__repr__() + 'COMMUNION\r\n' + \
            self.songs.pop(0).__repr__() + '\r\nSCRIPTURE READING\\SERMON\r\n' + \
            self.songs.pop(0).__repr__()

    def export_for_email_pm(self):
        pass
    
    def export_for_email_weds(self):
        pass

    def export_for_email_gospel_meeting(self):
        pass
