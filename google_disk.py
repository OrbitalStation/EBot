import json
import googleapiclient
import httplib2
import database as db
from googleapiclient.errors import HttpError
from json import JSONDecodeError
from oauth2client import clientsecrets, file
from oauth2client.client import OAuth2WebServerFlow, Credentials
from googleapiclient.discovery import build
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
    return build('drive', 'v2', http=http)


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


def upload_file(bot, message, file='document.txt', title='My New Text Document', description='A shiny new text document about hello world.',
                mimetype='text/plain'):
    # file: Path to the file to upload.

    drive_service = get_drive_service(bot, message)

    # Insert a file. Files are comprised of contents and metadata.
    # MediaFileUpload abstracts uploading file contents from a file on disk.
    media_body = googleapiclient.http.MediaFileUpload(
        file,
        mimetype=mimetype,
        resumable=True
    )
    # The body contains the metadata for the file.
    body = {
        'title': title,
        'description': description,
    }

    # Perform the request and print the result.
    try:
        new_file = drive_service.files().insert(
            body=body, media_body=media_body).execute()
        file_title = new_file.get('title')
        file_desc = new_file.get('description')
        if file_title == title and file_desc == description:
            print(f"File is uploaded \nTitle : {file_title}  \nDescription : {file_desc}")
            return True

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')
