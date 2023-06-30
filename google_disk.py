import json
import mimetypes
import os
import tempfile
import googleapiclient.http
import httplib2
import database as db
from json import JSONDecodeError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client import clientsecrets
from oauth2client.client import OAuth2WebServerFlow, Credentials
from properties import const


def get_drive_service(_bot, message):
    db.create_table_if_not_exists()
    user = db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=True)
    credentials = Credentials.new_from_json(user.google_disk_credentials)
    http = httplib2.Http()
    credentials.authorize(http)
    return build('drive', 'v3', http=http)


# noinspection PyProtectedMember
def get_flow(bot, message, client_secrets, scope) -> OAuth2WebServerFlow | None:
    try:
        cs = json.loads(client_secrets)
    except JSONDecodeError as err:
        bot.send_message(message.chat.id, const("botGDClientSecretsInvalidErrorMsg") % str(err))
        return
    try:
        cs_type, cs_info = clientsecrets._validate_clientsecrets(cs)
        if cs_type in (clientsecrets.TYPE_WEB,
                       clientsecrets.TYPE_INSTALLED):
            constructor_kwargs = {
                'redirect_uri': None,
                'auth_uri': cs_info['auth_uri'],
                'token_uri': cs_info['token_uri'],
                'login_hint': None,
            }
            revoke_uri = cs_info.get('revoke_uri')
            optional = (
                'revoke_uri',
                'device_uri',
                'pkce',
                'code_verifier',
                'prompt'
            )
            for param in optional:
                try:
                    if locals()[param] is not None:
                        constructor_kwargs[param] = locals()[param]
                except KeyError:
                    pass

            return OAuth2WebServerFlow(
                cs_info['client_id'], cs_info['client_secret'],
                scope, **constructor_kwargs)
    except clientsecrets.InvalidClientSecretsError as err:
        bot.send_message(message.chat.id, const("botGDClientSecretsInvalidErrorMsg") % str(err))
    else:
        bot.send_message(message.chat.id, const("googleOAuth2UnsupportedFlowErr") + ' ' + cs_type)
    return None


def upload_from_message(bot, message, **kwargs):
    """ Uploads content from message to Google Drive.
    bot: the bot
    message: message with photo or document
    **kwargs: custom filename or description for file
    Returns: id of the uploaded file
    """
    if message.content_type == "photo":
        file = message.photo[-1]
    elif message.content_type == "document":
        file = message.document
    else:
        return

    file_info = bot.get_file(file.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    tmp = tempfile.NamedTemporaryFile(dir=const("tempFilesPath"), delete=False)
    tmp.seek(0)
    tmp.write(downloaded_file)
    tmp.close()
    uploaded_id = upload_file(bot, message, tmp.name, **kwargs)
    os.unlink(tmp.name)
    return uploaded_id


def upload_file(bot, message, filepath, filename='Important', description='Uploaded by EmailBot'):
    db.create_table_if_not_exists()
    bot_folder_id = db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=True)\
        .google_disk_folder_id

    service = get_drive_service(bot, message)

    if not check_folder_exists(bot, message, service, bot_folder_id):
        bot.send_message(message.chat.id, const("GDFileUploadFolderNotExist"))
        return

    media_body = googleapiclient.http.MediaFileUpload(
        filename=filepath,
        mimetype=mimetypes.guess_type(filepath)[0],
        resumable=True
    )
    body = {
        'name': filename,
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
        if file_title == filename:
            bot.send_message(message.chat.id, const("GDFileUploadSuccess"))
            return new_file.get('id')
        else:
            bot.send_message(message.chat.id, const("GDFileUploadMaybeError") + f" {file_title} ~:~ {filename}")
    except HttpError as err:
        # TODO(developer) - Handle errors from drive API.
        bot.send_message(message.chat.id, const("GDFileUploadCreateError") + ' ' + str(err))


# def create_folder(bot, message, name, service):
#     try:
#         file_metadata = {
#             'name': name,
#             'mimeType': 'application/vnd.google-apps.folder'
#         }
#
#         bot.send_message(message.chat.id, const("GDFileUploadFolderCreateBegin") % name)
#
#         # pylint: disable=maybe-no-member
#         folder = service.files().create(body=file_metadata, fields='id').execute()
#         fid = folder.get("id")
#         bot.send_message(message.chat.id, const("GDFileUploadFolderCreated") % (name, fid))
#         return fid
#     except HttpError as err:
#         bot.send_message(message.chat.id, const("GDFileUploadFolderCreateError") % name + ' ' + str(err))
#         return


def check_folder_exists(bot, message, service, folder_id):
    try:
        response = service\
            .files()\
            .list(q=f"mimeType='application/vnd.google-apps.folder' and id='{folder_id}'", spaces='drive',).execute()
        return len(response.get('files', [])) > 0
    except HttpError as err:
        bot.send_message(message.chat.id, const("GDFileUploadCreateError") + ' ' + str(err))
        return None
