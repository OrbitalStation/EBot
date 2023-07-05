from database import db
from yadisk import YaDisk
from properties import const


def get_yadisk(bot, message):
    yandex_disk = db.fetch_user(message.from_user.id).storage.yandex_disk
    yy = YaDisk(token=yandex_disk.token.value, id=const("yaDiskID"), secret=const("yaDiskClientSecrets"))
    if not yy.check_token():
        bot.send_message(message.chat.id, const("botYDTokenInvalidAppTokenError"))
        return
    return yandex_disk, yy
