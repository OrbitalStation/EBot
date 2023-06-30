import os
import tempfile
from telebot.types import Message
from telebot import TeleBot
from google_drive.upload_raw_file import upload_raw_file
from properties import const


def upload_from_message(bot: TeleBot, message: Message, **kwargs):
    """ Uploads content from message to Google Drive.
    bot: the bot
    message: message with photo or document
    **kwargs: custom filename or description for file
    Returns: id of the uploaded file
    """
    if message.content_type in ['document', 'audio', 'voice', 'video', 'photo']:
        file = message.__getattribute__(message.content_type)
    else:
        return
    if message.content_type == "photo":
        file = file[-1]

    file_info = bot.get_file(file.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    tmp = tempfile.NamedTemporaryFile(dir=const("tempFilesPath"), delete=False)
    tmp.seek(0)
    tmp.write(downloaded_file)
    tmp.close()
    uploaded_id = upload_raw_file(bot, message, tmp.name, **kwargs)
    os.unlink(tmp.name)
    return uploaded_id
