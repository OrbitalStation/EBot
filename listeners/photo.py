import database as db
from listeners.__helper import listener
from properties import const
from e_mail.send import send
from google_disk import upload_from_message


@listener
def listener(bot, message):
    if file_id := upload_from_message(bot, message):
        file_url = const('googleDiskFilePrefix') + file_id
        caption = f"{file_url}</i><br><i>{message.caption if message.caption else ''}"
        if send(bot, message, db.fetch_user(message.from_user.id).email, caption):
            bot.send_message(message.chat.id, const("botPhotoSendToGDLis") + file_url)
            bot.send_message(message.chat.id, const("botMessageSentToEmailLis"))
    else:
        # TODO
        pass
