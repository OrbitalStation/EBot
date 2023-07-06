from listeners.__helper import listener
from properties import const
from e_mail.send import send
from database import db


@listener
def listener(bot, message):
    if send(bot, message, db.fetch_user(message.from_user.id).email, message.text, message.entities):
        bot.send_message(message.chat.id, const("botMessageSentToEmailLis"))
