from properties import const
from button import markup
from storage import CLOUD_STORAGE_BUTTONS
from database.interface import CloudStorage


def _con(bot, message, chosen):
    for field, ty in CloudStorage.__annotations__.items():
        if ty.__name__ == chosen:
            ty.configure(bot, message, path=['storage', field])
            break


def command(bot, message):
    bot.send_message(
        message.chat.id,
        const("botAddStorageChoiceCmd"),
        reply_markup=markup(bot, message, _con, CLOUD_STORAGE_BUTTONS))
