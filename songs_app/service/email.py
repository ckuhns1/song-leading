import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, body, senders_email, recipient_email, password):
        self.senders_email = senders_email
        self.recipient_email = recipient_email
        self.password = password
        self.subject = f'Songs--{self.get_date_of_sunday()}'
        self.body = body

    def preview(self):
        print("This is the email that will be sent:")
        print('', f'Subject: {self.subject}', f'Recipient: {self.recipient_email}', \
                '**************** Body ****************', self.body, sep='\r\n')

    def preview_and_send(self):
        self.preview()
        
        choice = input("Send? (y/n): ")
        if choice.lower() == 'y':
            check = input('type "yes" to confirm: ').strip()
            if check.lower() == 'yes':
                self.send_email(self.senders_email, self.password, self.recipient_email, self.subject, self.body)
        else:
            print("Email not sent.")

    def send_email(self, senders_email, sender_password, recipient_email, subject, body):
        try:
            # Set up the MIME
            message = MIMEMultipart()
            message['From'] = senders_email
            message['To'] = recipient_email
            message['Subject'] = subject

            # Attach the email body
            message.attach(MIMEText(body, 'plain'))

            # Connect to Gmail's SMTP server
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Upgrade the connection to secure
                server.login(senders_email, sender_password)  # Log in to your Gmail account
                server.send_message(message)  # Send the email

            print("Email sent successfully!")

        except Exception as e:
            print(f"Failed to send email: {e}")
    
    def get_date_of_sunday(self):
        today = datetime.date.today()
        day_of_week = today.weekday()
        days_until_sunday = (6 - day_of_week) % 7
        next_sunday = today + datetime.timedelta(days=days_until_sunday)

        return next_sunday.strftime('%-d %B %Y')  # Format as 'dd Month YYYY'