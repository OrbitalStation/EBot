import google_disk
from properties import const


def command(bot, message):
    bot.send_message(message.chat.id,
                     f"""Uploaded successful:\n
                     {const('googleDiskFilePrefix')}
                     {google_disk.upload_file(bot, message, 'rick.jpg')}""")
