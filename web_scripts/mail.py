import smtplib
from email.mime.text import MIMEText

def send(recipient, sender, subject, message):
    msg = MIMEText(message)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    s = smtplib.SMTP('outgoing.mit.edu', 25)
    s.sendmail(sender, [recipient], msg.as_string())
    s.quit()

