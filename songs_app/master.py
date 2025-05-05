from domain.assembly import Song, Service
from customize.hillview import Hillview
from service.email import Email
import os
from time import sleep


# instantiate service classes with service designs
morning = Service(Hillview().am_songs, Hillview().am_events)
evening = Service(Hillview().pm_songs, Hillview().pm_events)


# helper functions
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def apply_random_change(item, index):
    # Check if index is valid & alert user if not
    if not (1 <= index <= len(item.songs)):
        print("Invalid song number.")
        return
    
    song_to_change = item.order[index - 1] # get the position name of the song to be changed--see customize/service_layouts.py
    pool = getattr(item.pool, item.types[song_to_change]) # load the appropriate song pool
    if not pool:
        print("******SONG POOL EMPTY******\r\n"*3)
        sleep(2)
        return
    substitute = item.pool.pick_new_song_remove(pool) # pick a new song and remove it from the pool 
    setattr(item, song_to_change, Song(substitute)) # set the new song

def handle_search(item, index):
    if not (1 <= index <= len(item.songs)):
        print("Invalid song number.")
        return

    song_to_change = item.order[index - 1]
    search = input("Enter any part of song title to search: ").lower()
    pool = getattr(item.pool, item.types[song_to_change])
    matches = [s for s in pool if search in s[0].lower()]

    if not matches:
        print("No matches found.")
        return

    for i, (title, *_) in enumerate(matches, 1):
        print(f"({i}) {title}")

    pick = input('Enter number of song to insert, or "y" to cancel: ').strip()
    if pick.lower() == 'y':
        return

    if pick.isdigit() and 1 <= int(pick) <= len(matches):
        substitute = matches[int(pick) - 1]
        setattr(item, song_to_change, Song(substitute))
        item.pool.remove_song(pool, substitute)

def handle_manual_entry(item, index):
    if not (1 <= index <= len(item.songs)):
        print("Invalid song number.")
        return

    song_to_change = item.order[index - 1]
    title = input("Enter song title: ")
    number = input("Enter song number: ")
    verses = input("Enter verse numbers (space-separated, empty for all): ")
    chorus = input("Chorus at end only? (y/n): ").strip().lower() == 'y'
    
    new_song = Song([title, number, verses, '1' if chorus else '0', '', ''])
    setattr(item, song_to_change, new_song)

def change_verses(item, index):
    if not (1 <= index <= len(item.songs)):
        print("Invalid song number.")
        return
    
    verses = input("Enter new verse numbers (space-separated): ").strip()

    song_to_change = item.order[index - 1]
    song = getattr(item, song_to_change)
    song.verses = verses.split(' ') # set new verses
    setattr(item, song_to_change, song)

def change_chorus_end(item, index):
    if not (1 <= index <= len(item.songs)):
        print('Invalid song number.')
        return
    song_to_change = item.order[index - 1]
    song = getattr(item, song_to_change)
    song.chorus_at_end = not song.chorus_at_end
    setattr(item, song_to_change, song)

def swap_songs(item, index):
    if not (1 <= index <= len(item.songs)):
        print("Invalid song number.")
        return
    
    song1_to_swap = item.order[index - 1]
    index2 = int(input("Enter song number to swap with: ").strip())
    song2_to_swap = item.order[index2 - 1]

    song1 = getattr(item, song1_to_swap)
    song2 = getattr(item, song2_to_swap)
    setattr(item, song1_to_swap, song2)
    setattr(item, song2_to_swap, song1)

# main function applied to each Service
def prompt_change(item):
    while True:
        clear_terminal()
        item.export_for_revision()
        if item.has_duplicates():
            print('*************WARNING DUPLICATES IN LIST****************\r\n'*3)

        change_nbr = input('Enter #s to swap, #f find, #m manual add, #v verses, #c chorus at end, # random, y accept: ')
        if change_nbr.lower() == 'y':
            break
        elif change_nbr.isdigit():
            apply_random_change(item, int(change_nbr))
        elif 'f' in change_nbr:
            handle_search(item, int(change_nbr.replace('f', '')))
        elif 'm' in change_nbr:
            handle_manual_entry(item, int(change_nbr.replace('m', '')))
        elif 'v' in change_nbr:
            change_verses(item, int(change_nbr.replace('v', '')))
        elif 'c' in change_nbr:
            change_chorus_end(item, int(change_nbr.replace('c', '')))
        elif 's' in change_nbr:
            swap_songs(item, int(change_nbr.replace('s', '')))
        else:
            print('Invalid input. Please try again.')

# kick off song selection for each service
for item in [morning, evening]:
    prompt_change(item)            

# build email body
body = morning.export_for_email() + '\r\n__________________________________________\r\n\r\n' + \
    evening.export_for_email()

# pass email data to email class
email = Email(body, Hillview().email_info['senders_email'], Hillview().email_info['recipient_email'], Hillview().email_info['password'])

# preview and send email
clear_terminal()
email.preview_and_send()
