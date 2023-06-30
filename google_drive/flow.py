import json
from oauth2client import clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from properties import const


# noinspection PyProtectedMember
def get_flow(bot, message, client_secrets, scope) -> OAuth2WebServerFlow | None:
    try:
        cs = json.loads(client_secrets)
    except json.JSONDecodeError as err:
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
