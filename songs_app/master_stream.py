import streamlit as st
from domain.assembly import Song, Service
from customize.hillview import Hillview
from service.email import Email
import os
from time import sleep

st.set_page_config("Songs 4 U", layout="wide")
st.sidebar.header("Modify active service:")


if 'morning' not in st.session_state:
    st.session_state.morning = Service(Hillview().am_songs, Hillview().am_events)


# st.code(st.session_state.morning.export_for_revision(), language='text')
st.markdown(st.session_state.morning.export_for_revision())
    




def apply_random_change(item, index):
    # Check if index is valid & alert user if not
    if (1 <= index <= len(item.songs)):
    
        song_to_change = item.order[index - 1] # get the position name of the song to be changed--see customize/service_layouts.py
        pool = getattr(item.pool, item.types[song_to_change]) # load the appropriate song pool
        if not pool:
            st.text("******SONG POOL EMPTY******\r\n"*3)
            st.session_state.change_rand = ''
            return
        substitute = item.pool.pick_new_song_remove(pool) # pick a new song and remove it from the pool 
        setattr(item, song_to_change, Song(substitute)) # set the new song
        st.session_state.change_rand = ''

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

def change_verses(item, index, verses):
    if (1 <= index <= len(item.songs)):
        song_to_change = item.order[index - 1]
        song = getattr(item, song_to_change)

        song.verses = verses
        setattr(item, song_to_change, song)

def toggle_chorus(item, index):
    if (1 <= index <= len(item.songs)):
        song_to_change = item.order[index - 1]
        song = getattr(item, song_to_change)
        song.chorus_at_end = not song.chorus_at_end
        setattr(item, song_to_change, song)
        st.session_state.toggle_chorus = ''

def swap_songs(item, index):
    if all([(1 <= nbr <= len(item.songs)) for nbr in index]):
        song1_to_swap = item.order[index[0] - 1]
        song2_to_swap = item.order[index[1] - 1]

        song1 = getattr(item, song1_to_swap)
        song2 = getattr(item, song2_to_swap)
        setattr(item, song1_to_swap, song2)
        setattr(item, song2_to_swap, song1)

        st.session_state.swap = ''

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


def reset_list():
    del st.session_state['morning']
    st.session_state.morning = Service(Hillview().am_songs, Hillview().am_events)
    st.rerun()

def submit_rand():
    user_input = st.session_state.change_rand
    if user_input.isdigit():
        apply_random_change(st.session_state.morning, int(user_input))
    else: 
        st.session_state.change_rand = ''

def submit_chorus_toggle():
    user_input = st.session_state.toggle_chorus
    if user_input.isdigit():
        toggle_chorus(st.session_state.morning, int(user_input))
    else: 
        st.session_state.toggle_chorus = ''

def submit_swap():
    user_input = st.session_state.swap
    if ' ' in user_input and user_input.replace(' ', '').isdigit():
        temp = user_input.split(' ')
        user_input = list(map(int, temp))
        swap_songs(st.session_state.morning, user_input)
    else: 
        st.session_state.swap = ''

def submit_verses_change():
    user_input = st.session_state.verses
    temp = user_input.split(' ')
    user_input = list(map(int, temp))

    change_verses(st.session_state.morning, int(options.index(st.session_state.song_nbr)), st.session_state.verses)
    

if st.sidebar.button('Renew'):
    reset_list()

#### later, combine these into horiz. buttons and one text input
st.sidebar.text_input('Random #', key='change_rand', on_change=submit_rand)
st.sidebar.text_input('Toggle Chorus @ end', key='toggle_chorus', on_change=submit_chorus_toggle)
st.sidebar.text_input('Swap songs', key='swap', on_change=submit_swap)

# song selector
nbr_songs = len(st.session_state.morning.order)
options = [f"({i+1})" for i in range(nbr_songs)]

# Radio buttons in sidebar (horizontal style)
selected = st.sidebar.radio(
    "Select a song:",
    options,
    index=0,
    horizontal=True,
    key="song_nbr"
)

st.sidebar.text_input('Change verses', key='verses', on_change=submit_verses_change)













# build email body
# body = morning.export_for_email() + '\r\n__________________________________________\r\n\r\n' + \
#     evening.export_for_email()

# # pass email data to email class (set this info in customize/hillview.py)
# email = Email(body, Hillview().email_info['senders_email'], \
#               Hillview().email_info['recipient_email'], Hillview().email_info['password'])

# # preview and send email
# clear_terminal()
# email.preview_and_send()
