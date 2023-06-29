import google_disk


def command(bot, message):
    bot.send_document(message.chat.id, google_disk.upload_file(bot, message), visible_file_name="doc.txt")
