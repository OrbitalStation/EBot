from properties import const


def listener(cb):
    def inner(bot, message):
        if message.forward_from or message.forward_from_chat or message.forward_sender_name:
            cb(bot, message)
        else:
            print(message)
            bot.send_message(message.from_user.id, const("botNotForwardedMessageLis"))
    return inner
