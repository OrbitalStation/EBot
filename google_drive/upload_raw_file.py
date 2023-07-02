import mimetypes
import googleapiclient
from database import SQLiteDB as DB
from google_drive.service import get_drive_service
from googleapiclient.errors import HttpError
from properties import const


def upload_raw_file(bot, message, filepath, title, description='Uploaded by EmailBot'):
    DB.create_table_if_not_exists()
    bot_folder_id = DB.create_user_if_not_exists(message.from_user.id)\
        .google_disk_folder_id

    if (service := get_drive_service(bot, message)) is None:
        # TODO send_message
        return

    media_body = googleapiclient.http.MediaFileUpload(
        filename=filepath,
        mimetype=mimetypes.guess_type(filepath)[0],
        resumable=True
    )
    body = {
        'name': title,
        'description': description,
        'parents': [bot_folder_id]
    }

    try:
        new_file = service.files().create(
            uploadType="resumable",
            body=body,
            media_body=media_body
        ).execute()
        file_title = new_file.get('name')
        service.close()
        if file_title == title:
            bot.send_message(message.chat.id, const("GDFileUploadSuccess"))
            return new_file.get('id')
        else:
            bot.send_message(message.chat.id, const("GDFileUploadMaybeError") + f" {file_title} ~:~ {title}")
    except HttpError as err:
        # TODO(developer) - Handle errors from drive API.
        bot.send_message(message.chat.id, const("GDFileUploadCreateError") + ' ' + str(err))
