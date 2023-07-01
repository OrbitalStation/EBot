import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from properties import const


def send_raw(sender: str, sender_password: str, receiver: str, body: str, title: str):
    message = MIMEMultipart('alternative')
    message['Subject'] = title
    message['From'] = sender
    message['To'] = receiver

    message.attach(MIMEText("Важное", 'plain'))
    message.attach(MIMEText(body, 'html'))

    mail = smtplib.SMTP(const("SMTPHost"), int(const("SMTPPort")))
    mail.ehlo()
    if bool(const("SMTPDoStartTLS")):
        mail.starttls()
        mail.ehlo()
    if bool(const("botDoLoginEmail")):
        mail.login(sender, sender_password)

    errors = mail.sendmail(sender, receiver, message.as_string())
    mail.quit()
    return errors
