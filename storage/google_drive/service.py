import httplib2
from database import db
from oauth2client.client import Credentials
from googleapiclient.discovery import build
from json import JSONDecodeError
from properties import const


def get_drive_service(bot, message):
    user = db.fetch_user(message.from_user.id)
    try:
        credentials = Credentials.new_from_json(user.storage.google_drive.credentials.value)
    except JSONDecodeError as err:
        bot.send_message(message.chat.id, const("botUserInvalidCredentialsError") % str(err))
        return
    http = httplib2.Http()
    credentials.authorize(http)
    return build(const("googleService"), const("googleServiceVersion"), http=http)
