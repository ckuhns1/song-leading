import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

class Email:
    def __init__(self, body, senders_email, recipient_email, password):
        self.senders_email = senders_email
        self.recipient_email = recipient_email
        self.password = password
        self.subject = f'Songs--{self.get_date_of_sunday()}'
        self.body = body

    def preview(self):
        st.text( f'This is the email that will be sent:\r\n \
        ---------------------------------- \r\n\
        Subject: {self.subject} \r\n \
        Recipient: {self.recipient_email} \r\n \
        {self.body}'.replace('*', ''))

    def load_email_and_send(self):
        self.send_email(self.senders_email, self.password, self.recipient_email, self.subject, self.body)

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

            st.code("Email sent successfully!")

        except Exception as e:
            st.code(f"Failed to send email: {e}")
    
    def get_date_of_sunday(self):
        today = datetime.date.today()
        day_of_week = today.weekday()
        days_until_sunday = (6 - day_of_week) % 7
        next_sunday = today + datetime.timedelta(days=days_until_sunday)

        return next_sunday.strftime('%-d %B %Y')  # Format as 'dd Month YYYY'