from domain.assembly import Song, Service
from customize.service_layouts import Hillview
from customize.connection import email_info
from service.email import Email
import os

# This is the driver flow for the program

# instantiate service classes with service layouts
morning = Service(Hillview().am_songs, Hillview().am_events)
evening = Service(Hillview().pm_songs, Hillview().pm_events)


# sample and modify songs

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def apply_random_change(item, index):
    if not (1 <= index <= len(item.songs)):
        print("Invalid song number.")
        return
    
    song_to_change = item.order[index - 1]
    pool = getattr(item.pool, item.types[song_to_change])
    substitute = item.pool.pick_new_song_remove(pool)
    setattr(item, song_to_change, Song(substitute))

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
    
    verses = input("Enter new verse numbers (space-separated): ")

    song_to_change = item.order[index - 1]
    song = getattr(item, song_to_change)
    song.verses = verses.split(' ')
    setattr(item, song_to_change, song)

def change_chorus_end(item, index):
    if not (1 <= index <= len(item.songs)):
        print('Invalid song number.')
        return
    song_to_change = item.order[index - 1]
    song = getattr(item, song_to_change)
    song.chorus_at_end = not song.chorus_at_end
    setattr(item, song_to_change, song)

def prompt_change(item):
    while True:
        clear_terminal()
        item.export_for_revision()
        if item.has_duplicates():
            print('*************DUPLICATES IN LIST****************')

        change_nbr = input('Enter # to swap, #* search, #- specify song, #v change verses, #c change chorus at end, "y" accept: ')
        if change_nbr.lower() == 'y':
            break
        elif change_nbr.isdigit():
            apply_random_change(item, int(change_nbr))
        elif '*' in change_nbr:
            handle_search(item, int(change_nbr.replace('*', '')))
        elif '-' in change_nbr:
            handle_manual_entry(item, int(change_nbr.replace('-', '')))
        elif 'v' in change_nbr:
            change_verses(item, int(change_nbr.replace('v', '')))
        elif 'c' in change_nbr:
            change_chorus_end(item, int(change_nbr.replace('c', '')))
        else:
            print('Invalid input. Please try again.')

for item in [morning, evening]:
    prompt_change(item)            


body = morning.export_for_email() + '\r\n__________________________________________\r\n\r\n' + \
    evening.export_for_email()

email = Email(body, email_info.senders_email, email_info.recipient_email, email_info.password)

clear_terminal()
email.preview_and_send()
