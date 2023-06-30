from properties import const


def call(bot, message):
    bot.send_message(message.chat.id, const("botGreetingCmd"))
