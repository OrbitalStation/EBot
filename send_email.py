from forward_handlers import *
import smtplib
import time
from properties import const
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# bot.send_message(message.from_user.id, "Произошла ошибка при отправке письма")
def send_email(message, email, caption, links):
    EMAIL = const('botEmail')
    PASSWORD = const('botEmailPassword')

    if message.forward_from:
        chat, sender = forward_from(message)
    elif message.forward_from_chat:
        # Канал
        chat, sender = forward_from_chat(message)
    else:
        chat, sender = "", ""
        
    attachments = lambda: f'''
        <br>
        <b>Вложения:</b>
        <br>
        <i>{''.join(map(lambda x: f'<p>{x}</p>', links))}</i>'''
    
    attachments = attachments() if len(links) > 0 else ""
    
    body = f'''<b>ВАЖНОЕ - Вы отметили данное сообщение</b>
        <p><b>Чат:</b> <i>{chat}</i></p>
        <p><b>Отправитель:</b> <i>{sender}</i></p>
        <p><b>Время написания:</b> <i>{converted_time(message.forward_date)}</i></p>
        <b>Оригинальное сообщение:</b>
        <br>
        <i>{caption}</i>
        {attachments}
        '''
    
    html = f"""
        <html>
        <head></head>
        <body>
            <p>{body}</p>
        </body>
        </html>
        """

    message = MIMEMultipart('alternative')
    message['Subject'] = "Link"
    message['From'] = EMAIL
    message['To'] = email

    part1 = MIMEText("Важное", 'plain')
    part2 = MIMEText(html, 'html')

    message.attach(part1)
    message.attach(part2)

    mail = smtplib.SMTP('smtp.yandex.ru', 587)
    mail.ehlo()
    mail.starttls()
    mail.ehlo()
    mail.login(EMAIL, PASSWORD)

    mail.sendmail(EMAIL, email, message.as_string())
    mail.quit()


def converted_time(x):
    return time.strftime("%d.%M.%Y %H:%M:%S", time.localtime(x))
