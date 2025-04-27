from domain.hillview import AMSongs, PMSongs
from service.email import Email

# Running this script sends an email with the list of songs for the next Sunday; see details at bottom
body = AMSongs().export_for_email() + '\r\n\r\n' + PMSongs().export_for_email()
email = Email(body, 'chalkuhns@gmail.com')

# preview the email before sending
email.preview_and_send()