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
    search = input("Enter number or part of song title to search: ").lower()
    if search.isdigit():
        pool = getattr(item.pool, item.types[song_to_change])
        matches = [s for s in pool if search == s[1]]
    else: 
        pool = getattr(item.pool, item.types[song_to_change])
        matches = [s for s in pool if search in s[0].lower()]

    if not matches:
        print("*******No matches found*******\r\n"*3)
        sleep(2)
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

def list_songs(item, index):
    if not (1 <= index <= len(item.songs)):
        print("Invalid song number.")
        return
    
    song_to_change = item.order[index - 1]
    pool = getattr(item.pool, item.types[song_to_change]) # load the appropriate song pool

    if not pool:
        print("******SONG POOL EMPTY******\r\n"*3)
        sleep(2)
        return
    
    for i, song in enumerate(pool, 1):
        print(f'({i}){' '*(3-len(str(i)))} {song[1]}{' '*(3-len(song[1]))}  {song[0]}')

    pick = input('Enter number of song to insert, or "y" to cancel: ').strip()
    if pick.lower() == 'y':
        return
    
    if pick.isdigit() and 1 <= int(pick) <= len(pool):
        substitute = pool[int(pick) - 1]
        confirm = input(f'You selected {Song(substitute).__repr__()}. Enter "y" to confirm or "n" to escape: ').strip()
        if confirm.lower() == 'y':
            setattr(item, song_to_change, Song(substitute))
            item.pool.remove_song(pool, substitute)
        else: 
            return

def reset_list(item):
    item.__init__(item.types, item.events)
    pass

# main function applied to each Service
def prompt_change(item):
    """
    Interactively prompts the user to make changes to a given item through a series of options.

    The function repeatedly clears the terminal, displays the current state of the item for revision,
    and provides a menu of options for the user to modify the item. The loop continues until the user
    accepts the changes by entering 'y'.

    Args:
        item: The object to be modified. It must support the following methods:
            - export_for_revision(): Displays the current state of the item.
            - has_duplicates(): Returns a boolean indicating if there are duplicates in the item.

    User Input Options:
        - #s: Swap songs in the item.
        - #f: Find a song in the item.
        - #m: Manually add a song to the item.
        - #v: Change the verses of a song in the item.
        - #c: Move the chorus to the end of the item.
        - # random: Apply a random change to the item.
        - #l: List available options for the item.
        - r: Reset the item to its initial state.
        - y: Accept the current state of the item and exit the loop.

    Notes:
        - Input validation is performed, and invalid inputs prompt the user to try again.
        - If duplicates are detected in the item, a warning message is displayed.

    Raises:
        ValueError: If the input format is invalid for specific operations.
    """
    while True:
        clear_terminal()
        item.export_for_revision()
        if item.has_duplicates():
            print('*************WARNING: DUPLICATES IN LIST****************\r\n'*3)

        change_nbr = input('Enter #s swap, #f find, #m manual add, #v verses, ' +\
                           '#c chorus at end, # random, #l list options, r reset, y accept: ')
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
        elif 'l' in change_nbr:
            list_songs(item, int(change_nbr.replace('l', '')))
        elif 'r' in change_nbr:
            reset_list(item)
        else:
            print('Invalid input. Please try again.')

# kick off song selection for each service
for item in [morning, evening]:
    prompt_change(item)            

# build email body
body = morning.export_for_email() + '\r\n__________________________________________\r\n\r\n' + \
    evening.export_for_email()

# pass email data to email class (set this info in customize/hillview.py)
email = Email(body, Hillview().email_info['senders_email'], \
              Hillview().email_info['recipient_email'], Hillview().email_info['password'])

# preview and send email
clear_terminal()
email.preview_and_send()
