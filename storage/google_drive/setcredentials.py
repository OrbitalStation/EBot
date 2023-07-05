import oauth2client.client
from properties import const
from storage.google_drive.flow import get_flow


def _verification_code(bot, flow, path):
    def update(message):
        from commands.__helper import update_single_field
        credentials = flow.step2_exchange(message.text).to_json()
        update_single_field(bot, message, credentials, "_".join(path), const("botHumanGDCredentials"))
    return update


def _cs(bot, path):
    def update(message):
        from commands.__helper import user_answered
        if message.content_type == "text":
            flow = get_flow(bot, message, message.text, const("googleOauth2Scope"))
        elif message.content_type == "document":
            doc = message.document
            file_info = bot.get_file(doc.file_id)
            file_bytes = bot.download_file(file_info.file_path)
            flow = get_flow(bot, message, file_bytes.decode("utf-8"), const("googleOauth2Scope"))
        else:
            flow = None
        if flow is None:
            return
        flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
        authorize_url = flow.step1_get_authorize_url()
        bot.send_message(message.chat.id, const("botSetGDCredentialsExtraInfo3") + ' ' + authorize_url)
        message = bot.send_message(message.chat.id, const("botSetGDCredentialsExtraInfo4"))
        bot.register_next_step_handler(message, user_answered(bot, _verification_code(bot, flow, path), message,
                                                              const("botHumanGDClientSecrets")))
    return update


def set_credentials(bot, message, path):
    from commands.__helper import user_answered
    bot.send_message(message.chat.id, const("botSetGDCredentialsExtraInfo0"))
    message = bot.send_message(message.chat.id, const("botSetGDCredentialsExtraInfo1"))
    bot.register_next_step_handler(message, user_answered(bot, _cs(bot, path), message,
                                                          const("botHumanGDClientSecrets")))
