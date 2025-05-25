import streamlit as st
from domain.assembly import Song, Service
from customize.hillview import Hillview
from service.email import Email
from time import sleep


# setup page
st.set_page_config("Melody", layout="wide")

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
            sleep(2)
            st.session_state.emails.remove(email)
    
    
    if st.session_state.emails:
        st.balloons()
        sleep(2)
        st.session_state.email_setup = True
    else:
        st.session_state.address = ''



# Step 1: Enter/store email addresses
if 'email_setup' not in st.session_state:
    st.sidebar.info('To begin, please enter the email(s) you wish to send your addresses. Separate addresses with commas.')
    st.header('Songs List Recipient Email(s):')
    
    st.text_input(' ', key='address', on_change=save_email)


# initialize looping through services
if 'lineup' not in st.session_state:
    st.session_state.lineup = ['am', 'pm']
    st.session_state.settled = []
    lineup = st.session_state.lineup.copy()
    current = lineup.pop(0)
    st.session_state.current = current

    st.session_state.lineup = lineup
    st.session_state.active = Service(getattr(Hillview(), f'{current}_songs'), getattr(Hillview(), f'{current}_events'))
    st.session_state.finished_list = []

# helper functions


def advance_service():
    lineup = st.session_state.lineup.copy()
    if len(lineup) > 0:
        st.session_state.finished_list.append(st.session_state.active)
        st.session_state.current = lineup.pop(0)
        st.session_state.lineup = lineup

        current = st.session_state.current
        st.session_state.active = Service(getattr(Hillview(), f'{current}_songs'), getattr(Hillview(), f'{current}_events'))
        st.balloons()
        sleep(2)
        st.rerun()
    else: 
        st.session_state.finished_list.append(st.session_state.active)
        st.balloons()
        sleep(2)
        st.session_state.finalized = True
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

def start_over():
    for key in st.session_state.keys():
        del st.session_state[key]

    st.rerun()

def send_emails(address):
    # build email body
    body = '\r\n__________________________________________\r\n\r\n'.join([item.export_for_email() for item in st.session_state.finished_list])
    print(type(address))
    print(address)
    if isinstance(address, str):
        temp = Email(body, Hillview().email_info['senders_email'], \
                    address, Hillview().email_info['password'])
        temp.send_email()

    elif isinstance(address, list):
        for email in address:
            temp = Email(body, Hillview().email_info['senders_email'], \
                        email, Hillview().email_info['password'])
            temp.send_email()



# Step 2: Curate service lineups
if 'finalized' not in st.session_state and 'email_setup' in st.session_state:
    # show current service
    st.markdown(st.session_state.active.export_for_revision()) 



    # setup standard sidebar
    st.sidebar.info(f'Sending to: {', '.join(st.session_state.emails)}')
    st.sidebar.header("Service Actions:")
    col1, col2, col3 = st.sidebar.columns(3)
    renew_clicked = col1.button("Renew")
    accept_clicked = col2.button("Accept")
    restart = col3.button('Start Over')

    if accept_clicked:
        advance_service()

    if renew_clicked:
        reset_list()
    
    if restart:
        start_over()

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

    if random_clicked:
        submit_rand()

    if toggle_chorus_clicked:
        submit_chorus_toggle()

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

# Step 3: Send emails
elif 'finalized' in st.session_state:
    # email portal
    st.header('Email Portal')

    col1, col2 = st.columns(2)

    with col1:
        restart = st.button('Start Over')
        for email in st.session_state.emails:
            st.button(f'Email {email}', on_click=send_emails, args=(email,))
        print(st.session_state.emails)
        st.button(f'Email All', on_click=send_emails, args=(st.session_state.emails,))


    with col2:
        for item in st.session_state.finished_list:
            st.markdown(item.export_for_revision())
            st.markdown('---')
            st.markdown('---')
    
    if restart:
        start_over()
    









