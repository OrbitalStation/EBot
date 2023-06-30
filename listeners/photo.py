from listeners.__helper import listener
from properties import const
from google_disk import upload_from_message


@listener
def listener(bot, message):
    if file_id := upload_from_message(bot, message):
        # TODO sending to email ???
        text = const("botPhotoSendToGDLis") + ' ' + const('googleDiskFilePrefix') + file_id
        bot.send_message(message.from_user.id, text)
