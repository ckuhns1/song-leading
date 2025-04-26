from domain.hillview import AMSongs, PMSongs
from service.email import Email

# Running this script sends an email with the list of songs for the next Sunday; see details at bottom


if __name__ == "__main__":

    body = AMSongs().export_for_email_am() + '\r\n\r\n' + PMSongs().export_for_email_pm()

    email = Email(body, 'chalkuhns@gmail.com').preview()
