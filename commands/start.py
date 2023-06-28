from properties import const


def command(bot, message):
    bot.send_message(message.chat.id, const("botGreetingCmd"))
