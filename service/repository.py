import os

class Pool:
    def __init__(self):
        path = 'infra'
        for file_ in os.listdir(path):
            categ = file_.replace('.csv', '')
            with open(os.path.join(path, file_), 'r') as csv_file:
                songs = csv_file.readlines()
                setattr(self, categ, [song.strip() for song in songs if song.strip() != ''])

            

