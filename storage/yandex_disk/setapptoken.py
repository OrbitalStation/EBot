from yadisk import YaDisk
from yadisk.exceptions import BadRequestError
from properties import const
from convert_time_from_unix import convert
from time import time


def _concode(bot, yy, path):
    def update(message):
        from commands.__helper import update_single_field
        try:
            response = yy.get_token(message.text)
        except BadRequestError as err:
            bot.send_message(message.chat.id, const("botYDBadCodeError") % str(err))
            return
        yy.token = response.access_token
        if not yy.check_token():
            bot.send_message(message.chat.id, const("botYDTokenInvalidHowThough"))
            return
        bot.send_message(message.chat.id, const("botSetYDTokenSuccess") % convert(int(time()) + response.expires_in))
        update_single_field(bot, message, yy.token, "_".join(path), const("botHumanYDAppToken"))
    return update


def set_app_token(bot, message, path):
    from commands.__helper import user_answered
    yy = YaDisk(id=const("yaDiskID"), secret=const("yaDiskClientSecrets"))
    url = yy.get_code_url()
    message = bot.send_message(message.chat.id, const("botSetYDTokenAskForLink") + ' ' + url)
    bot.register_next_step_handler(message, user_answered(bot, _concode(bot, yy, path), message,
                                                          const("botHumanYDAppToken")))
