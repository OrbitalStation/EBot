from listeners.__helper import listener
from properties import const
from e_mail.send import send
from database import SQLiteDB as DB


@listener
def listener(bot, message):
    if send(bot, message, DB.fetch_user(message.from_user.id).email, message.text):
        bot.send_message(message.chat.id, const("botMessageSentToEmailLis"))
