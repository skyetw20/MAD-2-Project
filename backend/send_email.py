import os
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = 'skyetw20@outlook.com'

def send_email_function(subject, body, recipients, attachment_filename=None):#function to send email
    mailhog_server = 'localhost'
    mailhog_port = 1025
    for recipient in recipients:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        if attachment_filename:
            attachment_path = os.path.join('attachments', attachment_filename)
            if os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as attachment_file:
                    attachment = EmailMessage()
                    attachment.add_attachment(
                        attachment_file.read(),
                        maintype='application',
                        subtype='octet-stream',
                        filename=os.path.basename(attachment_path)
                    )
                msg.attach(attachment)
        with smtplib.SMTP(mailhog_server, mailhog_port) as server:
            server.sendmail(sender_email, recipient, msg.as_string())







