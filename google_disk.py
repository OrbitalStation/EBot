import json
import httplib2
import database as db
from json import JSONDecodeError
from oauth2client import clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from googleapiclient.discovery import build
from properties import const


def get_drive_service(bot, message):
    db.create_table_if_not_exists()
    user = db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=True)
    flow = get_flow(bot, message, user.google_disk_client_secrets, const("googleOauth2Scope"))
    credentials = flow.step2_exchange(user.google_disk_credentials)
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
                if locals()[param] is not None:
                    constructor_kwargs[param] = locals()[param]

            return OAuth2WebServerFlow(
                cs_info['client_id'], cs_info['client_secret'],
                scope, **constructor_kwargs)
    except clientsecrets.InvalidClientSecretsError as err:
        bot.send_message(message.chat.id, const("botGDClientSecretsInvalidErrorMsg") % str(err))
    else:
        bot.send_message(message.chat.id, const("googleOAuth2UnsupportedFlowErr") + ' ' + cs_type)
    return None

# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
#
#
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
#
#
# def upload(path, filename):
#     try:
#         drive = GoogleDrive(gauth)
#
#         file = drive.CreateFile({'title': f'{filename}'})
#         file.SetContentFile(path)
#         file.Upload()
#         file.InsertPermission({
#             'type': 'anyone',
#             'value': 'anyone',
#             'role': 'reader'})
#         link = file['alternateLink']
#         file = None
#
#         return link
#
#     except Exception:
#         return False
