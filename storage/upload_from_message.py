from database import db
from storage.google_drive.ufm import upload_from_message as gd


def upload_from_message(bot, message):
    {
        'GoogleDrive': gd
    }[db.fetch_user(message.from_user.id).storage.preferred](bot, message)
