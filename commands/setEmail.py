from properties import const
from parse_args import parse
import database as db


def command(bot, message):
    db.create_table_if_not_exists()
    db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=False)
    if (new_email := parse(message.text)) is None:
        bot.send_message(message.chat.id, const("botUserSetEmailNoArgErrorCmd"))
        return
    if '"' in new_email:
        bot.send_message(message.chat.id, const("botUserSetEmailQuoteInEmailErrorCmd"))
        return
    db.update_user(message.from_user.id, email=f'"{new_email}"')
    bot.send_message(message.chat.id, const("botUserSetEmailSuccessCmd") + ' ' + new_email)
