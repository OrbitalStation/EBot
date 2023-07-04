from properties import const
from button import markup
from storage import CLOUD_STORAGE_BUTTONS
from commands.__helper import update_single_field


def _con(bot, message, chosen):
    update_single_field(bot, message, chosen, 'storage_preferred', const("botHumanPreferredStorage"))


def command(bot, message):
    bot.send_message(
        message.chat.id,
        const("botButtonChoose") % const("botHumanPreferredStorage"),
        reply_markup=markup(bot, message, _con, CLOUD_STORAGE_BUTTONS))
