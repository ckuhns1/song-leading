import os
import sys
import random as rd

# used for PyInstaller references
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Pool:
    def __init__(self):
        """
        Initializes the repository by reading CSV files from the 'infra' directory.
        Dynamically sets attributes named after each CSV file (without the .csv extension).
        """
        path = resource_path('songs_app/infra')
        for file_ in os.listdir(path):
            if file_.endswith('.csv'):
                categ = file_.replace('.csv', '')
                file_path = os.path.join(path, file_)
                with open(file_path, 'r') as csv_file:
                    songs = csv_file.readlines()
                    songs = [song.strip().split(', ') for song in songs if song.strip()]
                    setattr(self, categ, sorted(songs, key=lambda x: x[0]))

    def pick_new_song_remove(self, group):
        """
        Selects a random song from the given group, removes it from the group, 
        and returns the selected song.

        Args:
            group (list): A list of songs to pick from.

        Returns:
            Any: The randomly selected song from the group.
        """
        song = rd.choice(group)
        group.remove(song)
        return song
    
    def remove_song(self, group, song):
        """
        Removes a specified song from the given group.

        Args:
            group (list): A list of songs to remove from.
            song (Any): The song to be removed from the group.
        """
        group.remove(song)