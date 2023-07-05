from properties import const
from storage.yandex_disk.service import get_yadisk
from yadisk.exceptions import ForbiddenError


def list_files(bot, message) -> list[str] | None:
    if (yyy := get_yadisk(bot, message)) is None:
        return
    yandex_disk, yy = yyy
    try:
        return list(map(lambda r: r.name, yy.listdir('/' + yandex_disk.folder_name.value)))
    except ForbiddenError as err:
        bot.send_message(message.chat.id, const("YDForbidden") % (const("YDPermissionRead"), str(err)))
        return
