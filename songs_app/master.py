from domain.hillview import Song, AMSongs, PMSongs
from service.email import Email

# instantiate song classes
morning = AMSongs()
evening = PMSongs()


# sample and modify AM songs
for item in [morning, evening]:
    item.export_for_revision() # print the list of songs for review
    change_nbr = input('Enter number of song to change, or "y" to accept: ')
    
    while change_nbr.lower() != 'y':
        if change_nbr.isdigit():
            change_nbr = int(change_nbr)
            if 1 <= change_nbr <= len(morning.songs):
                # switch the song with a given index
                setattr(item, item.order[change_nbr -1], \
                        Song(item.pool.pick(getattr(item.pool, item.types[item.order[change_nbr - 1]]))))

                print('New list of songs:')
                item.export_for_revision() # print the revised list for review

                change_nbr = input('Enter number of another song to change, or "y" to accept: ')
            else:
                print('Invalid choice. Please enter a number between 1 and', len(item.songs))
                change_nbr = input('Enter number of song to change, or "y" to accept: ')
        else:
            print('Invalid entry. Please enter "y" to accept, or a number between 1 and', len(item.songs))
            change_nbr = input('Enter number of song to change, or "y" to accept: ')



body = morning.export_for_email() + '\r\n__________________________________________\r\n\r\n' + \
    evening.export_for_email()
email = Email(body, 'chalkuhns@gmail.com')

email.preview_and_send()
