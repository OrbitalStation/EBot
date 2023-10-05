import smtplib

from telebot.types import Message, MessageEntity
from telebot import TeleBot
from convert_time_from_unix import convert
from properties import const
from e_mail import create_title_for_email_and_attachment
from .send_raw import send_raw
from .text2html import text2html


def send(bot: TeleBot, message: Message, email: str, caption: str, extra_caption: str, entities: list[MessageEntity] | None) -> bool:
    chat, sender = _get_chat_and_sender(message)
    chat = f"<p><b>Чат:</b> <i>{chat}</i></p>" if chat is not None else ""
    sender = f"<p><b>Отправитель:</b> <i>{sender}</i></p>" if sender is not None else ""
    time = convert(message.forward_date)
    caption = text2html(caption, entities)
    body = f"""
        <html><head></head><body>
        <b>ВАЖНОЕ - Вы отметили данное сообщение</b>
        {chat}
        {sender}
        <p><b>Время написания:</b> <i>{time}</i></p>
        <b>Оригинальное сообщение:</b>
        <br>
        <pre style="font-size:18px;">{caption}</pre>
        <br>
        <i>{extra_caption}</i>
        </body></html>
        """
    try:
        # TODO: `send_raw` returns a dict with possible errors. Deal with it
        send_raw(const("botEmail"), const("botEmailPassword"), email, body, create_title_for_email_and_attachment(time))
        return True
    except smtplib.SMTPRecipientsRefused as err:
        code, msg = err.recipients[email]
        if code == 501:
            key = const("botLetterSendInvalidEmailErrorMsg") % email
        else:
            key = msg.decode("utf-8")
        bot.send_message(message.chat.id, const("botLetterSendErrorPreamble") + ' ' + key)
        return False


def _get_chat_and_sender(message: Message) -> tuple[str | None, str | None]:
    if message.forward_from:
        # Chat
        return message.chat.first_name, message.forward_from.first_name + f' (@{message.forward_from.username})'
    elif message.forward_from_chat:
        if message.forward_signature:
            # Channel
            return message.forward_from_chat.title, message.forward_signature
        else:
            # Personal
            return None, message.forward_from_chat.title
    elif message.forward_sender_name:
        # IDK wtf is that but it pops up sometimes
        return None, message.forward_sender_name
    else:
        # Unknown
        return None, None
