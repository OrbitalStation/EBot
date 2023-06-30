import google_disk
from properties import const


# TODO getting GD botfolder link
def command(bot, message):
    fileid = google_disk.upload_file(bot, message, 'rick.jpg')
    bot.send_message(message.chat.id,
                     f"""Uploaded successful:\n
                     {const('googleDiskFilePrefix')}
                     {fileid}""")
    return fileid is not None   # validate?
