import httplib2
import database as db
from oauth2client.client import Credentials
from googleapiclient.discovery import build
from json import JSONDecodeError
from properties import const


def get_drive_service(bot, message):
    db.create_table_if_not_exists()
    user = db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=True)
    try:
        credentials = Credentials.new_from_json(user.google_disk_credentials)
    except JSONDecodeError as err:
        bot.send_message(message.chat.id, const("botUserInvalidCredentialsError") % str(err))
        return
    http = httplib2.Http()
    credentials.authorize(http)
    return build(const("googleService"), const("googleServiceVersion"), http=http)
