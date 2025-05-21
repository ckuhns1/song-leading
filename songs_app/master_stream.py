import streamlit as st
from domain.assembly import Song, Service
from customize.hillview import Hillview
from service.email import Email
from time import sleep


# setup page
st.set_page_config("Songs 4 U", layout="wide")
st.sidebar.header("Service Actions:")


# setup sidebar
col1, col2, col3 = st.sidebar.columns(3)
renew_clicked = col1.button("Renew")
accept_clicked = col2.button("Accept")
email_clicked = col3.button("Email")


# initialize looping through services
if 'lineup' not in st.session_state:
    st.session_state.lineup = ['am', 'pm']

if 'settled' not in st.session_state:
    st.session_state.settled = []


if 'current' not in st.session_state or accept_clicked:
    if st.session_state.lineup:

        if 'active' in st.session_state:
            st.session_state.settled.append(st.session_state.active)

        lineup = st.session_state.lineup.copy()
        st.session_state.current = lineup.pop(0)
        st.session_state.lineup = lineup

        current = st.session_state.current
        st.session_state.active = Service(getattr(Hillview(), f'{current}_songs'), getattr(Hillview(), f'{current}_events'))

    else:
        # initiate email handling
        st.session_state.settled.append(st.session_state.active)
        st.session_state.show = '---------------------------------\r\n\r\n'.join([''] + [item.export_for_email() for item in st.session_state.settled])
        body = st.session_state.show
        st.session_state.email = Email(body, Hillview().email_info['senders_email'], \
                Hillview().email_info['recipient_email'], Hillview().email_info['password'])
        st.session_state.email.preview()
        st.session_state.display_flag = False

# Radio buttons in sidebar (horizontal style)
st.sidebar.header('Song actions:')
nbr_songs = len(st.session_state.active.order)
options = [f"({i+1})" for i in range(nbr_songs)]

st.sidebar.radio(
    "Select a song:",
    options,
    index=0,
    horizontal=True,
    key="song_nbr"
)



# display active service
if 'display_flag' not in st.session_state:
    st.markdown(st.session_state.active.export_for_revision())

if email_clicked:
    body = st.session_state.show
    # pass email data to email class (set this info in customize/hillview.py)
    email = Email(body, Hillview().email_info['senders_email'], \
                Hillview().email_info['recipient_email'], Hillview().email_info['password'])

    # preview and send email
    email.send_email()
    




def apply_random_change(item, index):
    # Check if index is valid & alert user if not
    if (1 <= index <= len(item.songs)):
    
        song_to_change = item.order[index - 1] # get the position name of the song to be changed--see customize/service_layouts.py
        pool = getattr(item.pool, item.types[song_to_change]) # load the appropriate song pool
        if not pool:
            st.text("******SONG POOL EMPTY******\r\n"*3)
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

def change_verses(item, index, verses):
    if (1 <= index +1 <= len(item.songs)):
        song_to_change = item.order[index]
        song = getattr(item, song_to_change)
        song.verses = verses.split(' ')
        setattr(item, song_to_change, song)
        st.session_state.verses = ''

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
        print(f'({i}){" "*(3-len(str(i)))} {song[1]}{" "*(3-len(song[1]))}  {song[0]}')

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
    # del st.session_state['active']
    st.session_state.active = Service(
        getattr(Hillview(), f'{st.session_state.current}_songs'), 
        getattr(Hillview(), f'{st.session_state.current}_events'))
    st.rerun()

def submit_rand():
    user_input = st.session_state.song_nbr[1]
    apply_random_change(st.session_state.active, int(user_input))
    st.rerun()

def submit_chorus_toggle():
    user_input = st.session_state.song_nbr[1]
    toggle_chorus(st.session_state.active, int(user_input))
    st.rerun()

def submit_swap():
    user_input = st.session_state.swap
    if ' ' in user_input and user_input.replace(' ', '').isdigit():
        temp = user_input.split(' ')
        user_input = list(map(int, temp))
        swap_songs(st.session_state.active, user_input)
    else: 
        st.session_state.swap = ''

def submit_verses_change():
    user_input = st.session_state.verses

    change_verses(st.session_state.active, int(options.index(st.session_state.song_nbr)), user_input)
    st.session_state.verses = ''

    
if renew_clicked:
    reset_list()


col1, col2 = st.sidebar.columns(2)
random_clicked = col1.button('Random #')
toggle_chorus_clicked = col2.button('Toggle Chorus')

if random_clicked:
    submit_rand()

if toggle_chorus_clicked:
    submit_chorus_toggle()

st.sidebar.text_input('Swap two songs (space-separated):', key='swap', on_change=submit_swap)
    




st.sidebar.text_input('Select verses (space-separated):', key='verses', on_change=submit_verses_change)













# build email body
# body = morning.export_for_email() + '\r\n__________________________________________\r\n\r\n' + \
#     evening.export_for_email()

# # pass email data to email class (set this info in customize/hillview.py)
# email = Email(body, Hillview().email_info['senders_email'], \
#               Hillview().email_info['recipient_email'], Hillview().email_info['password'])

# # preview and send email
# clear_terminal()
# email.preview_and_send()
