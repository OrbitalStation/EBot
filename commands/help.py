from properties import const


def command(bot, message):
    for idx, line in enumerate(const("botHelpCmd").split('/')):
        if line != "":
            bot.send_message(message.chat.id, ('/' if idx > 0 else "") + line)
    bot.send_message(message.chat.id, const("botHelpForwardCmd"))
    bot.send_message(message.chat.id, const("botHelpWhatIfErrorCmd"))
    bot.send_message(message.chat.id, const("botHelpWhatIfCmdInsideCmd"))
    bot.send_message(message.chat.id, const("botHelpGoogleDiskCmd"))
    bot.send_message(message.chat.id, const("botHelpAddToContacts") % const("botEmail"))
