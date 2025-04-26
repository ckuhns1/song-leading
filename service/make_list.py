from service.repository import Pool
from domain.hillview import HtSongs, Song
import random as rd



def make_hillview_list_am(date):
    pool = Pool()

    singing = HtSongs(date)
    
    singing.songs.append(Song(rd.choice(pool.first)))
    singing.songs.append(Song(rd.choice(pool.prayer)))

    singing.songs.append(Song(rd.choice(pool.collection)))
    singing.songs.append(Song(rd.choice(pool.communion)))

    singing.songs.append(Song(rd.choice(pool.general)))
    singing.songs.append(Song(rd.choice(pool.invitation)))

    return singing.export_for_email_am()

def make_hillview_list_pm(date):
    pool = Pool()

    singing = HtSongs(date)
    
    singing.songs.append(Song(rd.choice(pool.first)))
    singing.songs.append(Song(rd.choice(pool.prayer)))

    singing.songs.append(Song(rd.choice(pool.general)))

    singing.songs.append(Song(rd.choice(pool.invitation)))
    singing.songs.append(Song(rd.choice(pool.communion)))

    return singing.export_for_email_pm()

def make_hillview_list_weds(date):
    pool = Pool()

    singing = HtSongs(date)
    singing.songs.append(Song(rd.choice(pool.general)))
    singing.songs.append(Song(rd.choice(pool.general)))

    singing.songs.append(Song(rd.choice(pool.invitation)))

    return singing.export_for_email_weds()

def make_hillview_list_gospel_meeting(date):
    return make_hillview_list_weds(date)

