import oauth2client.client
from commands.__helper import user_answered, update_single_field
from properties import const
from google_disk import get_flow
import database as db


def _update(bot, _message):
    def update(answer):
        update_single_field(bot, answer, answer.text, "google_disk_credentials", const('botHumanGDCredentials'))
    return update


def command(bot, message):
    db.create_table_if_not_exists()
    user = db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=True)
    flow = get_flow(bot, message, user.google_disk_client_secrets, const("googleOauth2Scope"))
    if flow is None:
        return
    flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
    authorize_url = flow.step1_get_authorize_url()
    bot.send_message(message.chat.id, const("botSetGDCredentialsExtraInfo1") + ' ' + authorize_url)
    message = bot.send_message(message.chat.id, const("botSetGDCredentialsExtraInfo2"))
    bot.register_next_step_handler(message, user_answered(bot, _update(bot, message), message, None,
                                                          const("botHumanGDCredentials")))
