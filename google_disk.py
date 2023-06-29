import json
import mimetypes
import os
import tempfile
from json import JSONDecodeError

import googleapiclient.http
import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client import clientsecrets
from oauth2client.client import OAuth2WebServerFlow, Credentials

import database as db
from properties import const

def get_drive_service(bot, message):
    # tools.run_flow
    # file.Storage
    db.create_table_if_not_exists()
    user = db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=True)
    # flow = get_flow(bot, message, user.google_disk_client_secrets, const("googleOauth2Scope"))
    # if flow is None:
    #     return None
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
    **kwargs: custom title or description for file
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
    tmp = tempfile.NamedTemporaryFile(dir=const("tempfilesPath"), delete=False)
    tmp.seek(0)
    tmp.write(downloaded_file)
    tmp.close()
    uploaded_id = upload_file(bot, message, tmp.name, **kwargs)
    os.unlink(tmp.name)
    return uploaded_id


def upload_file(bot, message, filepath, title='Generic', description='Uploaded by EmailBot'):
    # filepath: Path to the file to upload.
    print(db.fetch_user(message.chat.id).bot_folder_id)
    if not check_bot_folder_exists(bot, message):
        print("Folder not found, making new folder...")
        folder_id = make_bot_folder(bot, message)
        db.update_user(message.chat.id, bot_folder_id=folder_id)
    else:
        # Warning! Fetched id might be invalid (there are no checks)
        folder_id = db.fetch_user(message.chat.id).bot_folder_id

    drive_service = get_drive_service(bot, message)

    # Insert a file. Files are comprised of contents and metadata.
    # MediaFileUpload abstracts uploading file contents from a file on disk.
    media_body = googleapiclient.http.MediaFileUpload(
        filename=filepath,
        mimetype=mimetypes.guess_type(filepath)[0],
        resumable=True
    )
    # The body contains the metadata for the file.
    body = {
        'name': title,
        'description': description,  # Unnecessary field
        'parents': [folder_id]
    }

    # Perform the request and print the result.
    try:
        new_file = drive_service.files().create(
            uploadType="resumable",
            body=body,
            media_body=media_body
        ).execute()
        file_title = new_file.get('name')
        # For downloading bytes:
        # request = drive_service.files().get_media(fileId=new_file.get("id")).execute()

        drive_service.close()
        if file_title == title:
            print(f"File is uploaded : {new_file}")
            return new_file.get('id')
        else:
            print(f"Upload may be unsuccessful!\n{file_title} ~:~ {title}")

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def make_bot_folder(bot, message):
    try:
        # create drive api client
        service = get_drive_service(bot, message)
        file_metadata = {
            'name': const("botFolderName"),
            'mimeType': 'application/vnd.google-apps.folder'
        }

        # pylint: disable=maybe-no-member
        folder = service.files().create(body=file_metadata, fields='id'
                                        ).execute()
        print(F'Made folder with ID: "{folder.get("id")}".')
        return folder.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


def check_bot_folder_exists(bot, message):
    return check_folder_exists(bot, message, const("botFolderName"))


def check_folder_exists(bot, message, folder_name):
    try:
        # create drive api client
        service = get_drive_service(bot, message)
        folders = []
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
            for folder in response.get('files', []):
                # Process change
                print(F'Found folder: {folder.get("name")}, {folder.get("id")}')
            folders.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None or len(folders) != 0:
                break

    except HttpError as error:
        print(F'An error occurred: {error}')
        folders = None

    return len(folders) != 0
