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
        st.text(f'---------------------------------- \r\nSubject: {self.subject} \r\n{self.body}'.replace('*', ''))

    def load_email_and_send(self):
        for email in st.session_state.parsed:
            self.send_email(self.senders_email, self.password, email, self.subject, self.body)

    def send_email(self):
        try:
            # Set up the MIME
            message = MIMEMultipart()
            message['From'] = self.senders_email
            message['To'] = self.recipient_email
            message['Subject'] = self.subject

            # Attach the email body
            message.attach(MIMEText(self.body, 'plain'))

            # Connect to Gmail's SMTP server
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Upgrade the connection to secure
                server.login(self.senders_email, self.password)  # Log in to your Gmail account
                server.send_message(message)  # Send the email

            st.code(f"Email sent successfully to {self.recipient_email}!")

        except Exception as e:
            st.code(f"Failed to send email to {self.recipient_email}: {e}")
    
    def get_date_of_sunday(self):
        today = datetime.date.today()
        day_of_week = today.weekday()
        days_until_sunday = (6 - day_of_week) % 7
        next_sunday = today + datetime.timedelta(days=days_until_sunday)

        return next_sunday.strftime('%-d %B %Y')  # Format as 'dd Month YYYY'