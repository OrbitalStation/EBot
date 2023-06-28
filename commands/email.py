from properties import const
import database as db


def command(bot, message):
    db.create_table_if_not_exists()
    user = db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=True)
    if user.email == "":
        bot.send_message(message.chat.id, const("botUserHasNoEmailCmd"))
    else:
        bot.send_message(message.chat.id, const("botUserHasEmailCmd") + ' ' + user.email)
