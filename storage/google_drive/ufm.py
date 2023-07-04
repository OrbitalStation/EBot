import os
import tempfile
from os.path import exists, isdir
from telebot.types import Message
from telebot import TeleBot
from storage.google_drive.upload_raw_file import upload_raw_file
from e_mail import create_title_for_email_and_attachment
from convert_time_from_unix import convert
from properties import const


def upload_from_message(bot: TeleBot, message: Message) -> int | None:
    """ Uploads content from message to Google Drive.
    bot: the bot
    message: message with photo or document
    Returns: id of the uploaded file
    """
    if message.content_type in ['document', 'audio', 'voice', 'video', 'photo']:
        file = message.__getattribute__(message.content_type)
    else:
        return
    if message.content_type == "photo":
        file = file[-1]

    if not exists(const("tempFilesPath")):
        os.mkdir(const("tempFilesPath"))
    elif not isdir(const("tempFilesPath")):
        os.unlink(const("tempFilesPath"))
        os.mkdir(const("tempFilesPath"))

    file_info = bot.get_file(file.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    tmp = tempfile.NamedTemporaryFile(dir=const("tempFilesPath"), delete=False)
    tmp.seek(0)
    tmp.write(downloaded_file)
    tmp.close()
    uploaded_id = upload_raw_file(bot, message, tmp.name,
                                  create_title_for_email_and_attachment(convert(message.forward_date)))
    os.unlink(tmp.name)
    return uploaded_id
