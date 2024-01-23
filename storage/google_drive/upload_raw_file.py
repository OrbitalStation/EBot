import mimetypes
import googleapiclient
from database import db
from storage.google_drive.service import get_drive_service
from googleapiclient.errors import HttpError
from properties import const
from urllib.parse import quote


def upload_raw_file(bot, message, filepath, title, description='Uploaded by EmailBot') -> str | None:
    bot_folder_id = db.fetch_user(message.from_user.id).storage.google_drive.folder_id.value

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
        bot.send_message(message.chat.id, const("GDFileUploadStart"))
        new_file = service.files().create(
            uploadType="resumable",
            body=body,
            media_body=media_body
        ).execute()
        file_title = new_file.get('name')
        service.close()
        if file_title == title:
            bot.send_message(message.chat.id, const("FileUploadSuccess"))
            return const("googleDiskFilePrefix") + quote(new_file.get('id'), safe="")
        else:
            bot.send_message(message.chat.id, const("GDFileUploadMaybeError") + f" {file_title} ~:~ {title}")
    except HttpError as err:
        if "File not found" in str(err):
            bot.send_message(message.chat.id, const("GDFileUploadFolderNotExist"))
        else:
            # TODO(developer) - Handle errors from drive API.
            bot.send_message(message.chat.id, const("GDFileUploadCreateError") + ' ' + str(err))
