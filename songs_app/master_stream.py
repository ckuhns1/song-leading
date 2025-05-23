import streamlit as st
from domain.assembly import Song, Service
from customize.hillview import Hillview
from service.email import Email
from time import sleep


# setup page
st.set_page_config("Melody", layout="wide")

# initialize looping through services
if 'lineup' not in st.session_state:
    st.session_state.lineup = ['am', 'pm']
    st.session_state.settled = []
    lineup = st.session_state.lineup.copy()
    current = lineup.pop(0)
    st.session_state.current = current

    st.session_state.lineup = lineup
    st.session_state.active = Service(getattr(Hillview(), f'{current}_songs'), getattr(Hillview(), f'{current}_events'))


# helper functions
def save_email():
    temp = st.session_state.address
    temp = temp.split(',')
    st.session_state.emails = list(map(lambda x: x.strip(), temp))

    for email in st.session_state.emails:
        cond1 = ('@' in email)
        cond2 = ('.' in email)
        if all([cond1, cond2]):
            placeholder = st.empty()

            with placeholder:
                st.info(f'Email {email} stored')
            
            sleep(2)
            placeholder.empty()
        else:
            st.info(f'{email} is not a valid email address. Removing it from the recipient list.')
            st.session_state.emails.remove(email)
    
    
    if st.session_state.emails:
        st.balloons()
        sleep(2)
        st.session_state.email_setup = True
    else:
        st.session_state.address = ''

def advance_service():
    lineup = st.session_state.lineup.copy()
    st.session_state.current = lineup.pop(0)
    st.session_state.lineup = lineup

    current = st.session_state.current
    st.session_state.active = Service(getattr(Hillview(), f'{current}_songs'), getattr(Hillview(), f'{current}_events'))
    st.balloons()
    sleep(2)
    st.rerun()

def reset_list():
    del st.session_state['active']
    st.session_state.active = Service(
        getattr(Hillview(), f'{st.session_state.current}_songs'), 
        getattr(Hillview(), f'{st.session_state.current}_events'))
    st.rerun()

def apply_random_change(item, index):
    # Check if index is valid & alert user if not
    if (1 <= index <= len(item.songs)):
    
        song_to_change = item.order[index - 1] # get the position name of the song to be changed--see customize/service_layouts.py
        pool = getattr(item.pool, item.types[song_to_change]) # load the appropriate song pool
        if not pool:
            st.sidebar.header("!!!SONG POOL EMPTY!!!")
            st.sidebar.header("!!!SONG POOL EMPTY!!!")
            st.sidebar.header("!!!SONG POOL EMPTY!!!")

            sleep(2)
            return
        substitute = item.pool.pick_new_song_remove(pool) # pick a new song and remove it from the pool 
        setattr(item, song_to_change, Song(substitute)) # set the new song

def submit_rand():
    user_input = st.session_state.song_nbr[1]
    apply_random_change(st.session_state.active, int(user_input))
    st.rerun()

def toggle_chorus(item, index):
    if (1 <= index <= len(item.songs)):
        song_to_change = item.order[index - 1]
        song = getattr(item, song_to_change)
        song.chorus_at_end = not song.chorus_at_end
        setattr(item, song_to_change, song)
        st.session_state.toggle_chorus = ''

def submit_chorus_toggle():
    user_input = st.session_state.song_nbr[1]
    toggle_chorus(st.session_state.active, int(user_input))
    st.rerun()

def swap_songs(item, index):
    if all([(1 <= nbr <= len(item.songs)) for nbr in index]):
        song1_to_swap = item.order[index[0] - 1]
        song2_to_swap = item.order[index[1] - 1]

        song1 = getattr(item, song1_to_swap)
        song2 = getattr(item, song2_to_swap)
        setattr(item, song1_to_swap, song2)
        setattr(item, song2_to_swap, song1)

        st.session_state.swap = ''

def submit_swap():
    user_input = st.session_state.swap
    if user_input.strip().isdigit():
        user_input1 = int(user_input)
        user_input2 = int(st.session_state.song_nbr[1])
        pair = [user_input1, user_input2]
        swap_songs(st.session_state.active, pair)
    else: 
        st.session_state.swap = ''

def manual():
    song_to_change = st.session_state.active.order[int(st.session_state.song_nbr[1]) - 1]
    title = st.session_state.title
    number = st.session_state.number
    
    new_song = Song([title, number, '', '', ''])
    setattr(st.session_state.active, song_to_change, new_song)

def change_verses(item, index, verses):
    if (1 <= index +1 <= len(item.songs)):
        song_to_change = item.order[index]
        song = getattr(item, song_to_change)
        song.verses = verses.split(' ')
        setattr(item, song_to_change, song)
        st.session_state.verses = ''

def submit_verses_change():
    user_input = st.session_state.verses

    change_verses(st.session_state.active, int(options.index(st.session_state.song_nbr)), user_input)
    st.session_state.verses = ''

def handle_search():
    pass

# Step 1: Enter/store email addresses
if 'email_setup' not in st.session_state:
    st.sidebar.info('To begin, please enter the email(s) you wish to send your addresses. Separate addresses with commas.')
    st.header('Songs List Recipient Email(s):')
    
    st.text_input(' ', key='address', on_change=save_email)
    st.rerun()


# Step 2: Curate service lineups
if 'list_build' not in st.session_state:
    # show current service
    if 'search' not in st.session_state:
        st.markdown(st.session_state.active.export_for_revision()) 
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.header('Column 1')
            st.markdown(st.session_state.active.export_for_revision()) 
        with col2:
            st.header('Column 2')
            st.button('Text', key='123')
            st.markdown(st.session_state.active.export_for_revision()) 
        del st.session_state['search']



    # setup standard sidebar
    st.sidebar.header("Service Actions:")
    col1, col2 = st.sidebar.columns(2)
    renew_clicked = col1.button("Renew")
    accept_clicked = col2.button("Accept")

    st.sidebar.markdown('---')

    st.sidebar.header("Song Actions:")
    options = [f'({i+1})' for i in range(len(st.session_state.active.order))]
    st.sidebar.radio(
        "Select a song to modify:",
        options,
        index=0,
        horizontal=True,
        key="song_nbr"
    )

    col1, col2 = st.sidebar.columns(2)
    random_clicked = col1.button('Random')
    toggle_chorus_clicked = col2.button('Chorus')
    st.sidebar.text_input('Swap with song number:', key='swap', on_change=submit_swap)
    st.sidebar.text_input('List verses, space-separated:', key='verses', on_change=submit_verses_change)

    st.sidebar.markdown('---')

    st.sidebar.header('Manual Entry')

    st.sidebar.text_input('Title:', key='title')
    st.sidebar.text_input('Number:', key='number')

    # Only show Submit if both fields are filled
    if st.session_state.get('title') and st.session_state.get('number'):
        if st.sidebar.button('Submit'):
            manual()
            st.session_state['manual_add_active'] = ''
            st.rerun()

    st.sidebar.markdown('---')

    st.sidebar.header('Search')

    st.sidebar.text_input('Search by number or title:', key='search', on_change=handle_search)



    if accept_clicked:
        advance_service()

    if renew_clicked:
        reset_list()

    if random_clicked:
        submit_rand()

    if toggle_chorus_clicked:
        submit_chorus_toggle()
    













# def handle_search(item, index):
#     if not (1 <= index <= len(item.songs)):
#         print("Invalid song number.")
#         return

#     song_to_change = item.order[index - 1]
#     search = input("Enter number or part of song title to search: ").lower()
#     if search.isdigit():
#         pool = getattr(item.pool, item.types[song_to_change])
#         matches = [s for s in pool if search == s[1]]
#     else: 
#         pool = getattr(item.pool, item.types[song_to_change])
#         matches = [s for s in pool if search in s[0].lower()]

#     if not matches:
#         print("*******No matches found*******\r\n"*3)
#         sleep(2)
#         return

#     for i, (title, *_) in enumerate(matches, 1):
#         print(f"({i}) {title}")

#     pick = input('Enter number of song to insert, or "y" to cancel: ').strip()
#     if pick.lower() == 'y':
#         return

#     if pick.isdigit() and 1 <= int(pick) <= len(matches):
#         substitute = matches[int(pick) - 1]
#         setattr(item, song_to_change, Song(substitute))
#         item.pool.remove_song(pool, substitute)









# def list_songs(item, index):
#     if not (1 <= index <= len(item.songs)):
#         print("Invalid song number.")
#         return
    
#     song_to_change = item.order[index - 1]
#     pool = getattr(item.pool, item.types[song_to_change]) # load the appropriate song pool

#     if not pool:
#         print("******SONG POOL EMPTY******\r\n"*3)
#         sleep(2)
#         return
    
#     for i, song in enumerate(pool, 1):
#         print(f'({i}){" "*(3-len(str(i)))} {song[1]}{" "*(3-len(song[1]))}  {song[0]}')

#     pick = input('Enter number of song to insert, or "y" to cancel: ').strip()
#     if pick.lower() == 'y':
#         return
    
#     if pick.isdigit() and 1 <= int(pick) <= len(pool):
#         substitute = pool[int(pick) - 1]
#         confirm = input(f'You selected {Song(substitute).__repr__()}. Enter "y" to confirm or "n" to escape: ').strip()
#         if confirm.lower() == 'y':
#             setattr(item, song_to_change, Song(substitute))
#             item.pool.remove_song(pool, substitute)
#         else: 
#             return











    



# def search_pool():
#     user_input = int(st.session_state.song_nbr[1])
#     print(user_input)
#     search_str = st.session_state.search
#     matches = st.session_state.active.search_pool(user_input, search_str)

    
#     st.sidebar.markdown('\r\n'.join([Song(item).__repr__() for item in matches]))
