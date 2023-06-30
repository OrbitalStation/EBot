import oauth2client.client
from commands.__helper import user_answered, update_single_field
from properties import const
from google_disk import get_flow
from commands.__helper import send_markdown
import database as db


def _verification_code(bot, flow):
    def update(message):
        db.create_table_if_not_exists()
        db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=False)
        credentials = flow.step2_exchange(message.text).to_json()
        update_single_field(bot, message, credentials, "google_disk_credentials", const('botHumanGDCredentials'))
        bot.send_message(message.chat.id, const("botUserSetterSuccessCmd") % const("botHumanGDCredentials") +
                         ' ' + credentials)
    return update


def _cs(bot):
    def update(message):
        if message.content_type == "text":
            flow = get_flow(bot, message, message.text, const("googleOauth2Scope"))
        elif message.content_type == "document":
            doc = message.document
            file_info = bot.get_file(doc.file_id)
            file_bytes = bot.download_file(file_info.file_path)
            flow = get_flow(bot, message, file_bytes.decode("utf-8"), const("googleOauth2Scope"))

        if flow is None:
            return
        flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
        authorize_url = flow.step1_get_authorize_url()
        bot.send_message(message.chat.id, const("botSetGDCredentialsExtraInfo3") + ' ' + authorize_url)
        message = bot.send_message(message.chat.id, const("botSetGDCredentialsExtraInfo4"))
        bot.register_next_step_handler(message, user_answered(bot, _verification_code(bot, flow), message, None,
                                                              const("botHumanGDCredentials")))
    return update


def call(bot, message):
    bot.send_message(message.chat.id, const("botSetGDCredentialsExtraInfo0"))
    bot.send_message(message.chat.id, const("botSetGDCredentialsExtraInfo1"))
    bot.register_next_step_handler(message, user_answered(bot, _cs(bot), message, None,
                                                          const("botHumanGDClientSecrets")))
