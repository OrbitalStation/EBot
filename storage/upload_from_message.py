import os
import tempfile
from os.path import exists, isdir
from convert_time_from_unix import convert
from database import db
from e_mail import create_title_for_email
from properties import const
from storage.google_drive.upload_raw_file import upload_raw_file as gd
from storage.yandex_disk.upload_raw_file import upload_raw_file as yd
from storage.yandex_disk.list_files import list_files as ydlist
from dataclasses import dataclass
from typing import Callable, Optional, Any
from telebot import TeleBot
from telebot.types import Message
from threading import Lock


@dataclass(frozen=True, kw_only=True)
class RawSender:
    callback: Callable[[TeleBot, Message, str, str], Optional[str]]
    list_files_or_can_duplicate: Optional[Callable[[TeleBot, Message], list[str]]]


RAW = {
    'GoogleDrive': RawSender(callback=gd, list_files_or_can_duplicate=None),
    'YandexDisk': RawSender(callback=yd, list_files_or_can_duplicate=ydlist)
}


@dataclass(init=False)
class MaxFilenameTagWatcher:
    lock: Any
    maximum: int

    def __init__(self):
        self.lock = Lock()
        self.maximum = 0


def upload_from_message(bot: TeleBot, message: Message, watcher: MaxFilenameTagWatcher) -> Optional[str]:
    try:
        raw_sender = RAW[db.fetch_user(message.from_user.id).storage.preferred]
    except KeyError:
        bot.send_message(message.chat.id, const("botHelpGoogleDiskCmd"))
        return
    return _upload(bot, message, raw_sender, watcher)


def _upload(bot: TeleBot, message: Message, raw_sender: RawSender, watcher: MaxFilenameTagWatcher) -> Optional[str]:
    """ Uploads content from message to cloud storage.
    bot: the bot
    message: message with photo or document
    raw_sender: and interface of the cloud storage
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

    try:
        title = file.file_name
    except AttributeError:
        title = message.content_type.capitalize()
    title = create_title_for_email(title, convert(message.forward_date))

    if raw_sender.list_files_or_can_duplicate is not None:
        with watcher.lock:
            maximum = watcher.maximum
            if (lst := raw_sender.list_files_or_can_duplicate(bot, message)) is None:
                return
            for file in lst:
                try:
                    maximum = max(get_integer_prefix_if_any(file), maximum)
                except ValueError:
                    pass
            watcher.maximum = maximum + 1
            title = str(watcher.maximum).zfill(4) + ' ' + title

    returned = raw_sender.callback(bot, message, tmp.name, title)
    os.unlink(tmp.name)
    return returned


def get_integer_prefix_if_any(s: str) -> Optional[int]:
    found = len(s)
    for idx, ch in enumerate(s):
        if not ch.isdigit():
            found = idx
            break
    return int(s[:found])
