from listeners.__helper import listener
from properties import const
from google_disk import upload_from_message
from e_mail.send import send
import database as db


@listener
def listener(bot, message):
    if (file_id := upload_from_message(bot, message)) is None:
        return
    text = const("botPhotoSendToGDLis") + ' ' + const("googleDiskFilePrefix") + file_id
    if send(bot, message, db.fetch_user(message.from_user.id).email, text):
        bot.send_message(message.from_user.id, const("botMessageSentToEmailLis"))
