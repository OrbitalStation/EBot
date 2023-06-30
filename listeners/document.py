import database as db
from e_mail.send import send
from listeners.__helper import listener
from properties import const
from google_disk import upload_from_message


@listener
def listener(bot, message):
    if file_id := upload_from_message(bot, message, filename=message.document.file_name):
        file_url = const('googleDiskFilePrefix') + file_id
        caption = f"{file_url}</i><br><i>{message.caption if message.caption else ''}"
        if send(bot, message, db.fetch_user(message.from_user.id).email, caption):
            bot.send_message(message.chat.id, const("botDocSendToGDLis") + file_url)
            bot.send_message(message.chat.id, const("botMessageSentToEmailLis"))
    else:
        # TODO
        pass