import google_disk


def command(bot, message):
    bot.send_message(message.chat.id, google_disk.upload_file(bot, message))
