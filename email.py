import smtplib
import os
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from make_list import make_hillview_list_am


def get_date_of_sunday():
    today = datetime.date.today()
    day_of_week = today.weekday()
    days_until_sunday = (6 - day_of_week) % 7
    next_sunday = today + datetime.timedelta(days=days_until_sunday)
    return next_sunday.strftime('%d %B %Y')  # Format as YYYY-MM-DD


def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Attach the email body
        message.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, sender_password)  # Log in to your Gmail account
            server.send_message(message)  # Send the email

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
if __name__ == "__main__":
    sender_email = "chalkuhns@gmail.com"  # Replace with your Gmail address
    sender_password = os.getenv('GM_PWD')      # Replace with your Gmail password or app password
    recipient_email = "chalkuhns@gmail.com"  # Replace with the recipient's email address
    

    subject = f'Songs {get_date_of_sunday()}'
    body = make_hillview_list_am(get_date_of_sunday())

    send_email(sender_email, sender_password, recipient_email, subject, body)
