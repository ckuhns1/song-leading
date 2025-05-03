import os
import random as rd

class Pool:
    def __init__(self):
        """
        Initializes the repository by reading CSV files from the 'infra' directory.
        
        For each CSV file in the 'infra' directory:
        - The file name (without the '.csv' extension) is used as an attribute name.
        - The contents of the file are read, with each line split by ', ' and stored as a list of lists.
        - Empty lines in the file are ignored.

        Attributes:
            Dynamically creates attributes for each CSV file in the 'infra' directory,
            where the attribute name corresponds to the file name (without the '.csv' extension),
            and the value is a list of lists representing the file's contents.
        """
        path = 'infra'
        for file_ in os.listdir(path):
            categ = file_.replace('.csv', '')
            with open(os.path.join(path, file_), 'r') as csv_file:
                songs = csv_file.readlines()
                setattr(self, categ, [song.strip().split(', ') for song in songs if song.strip() != ''])

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