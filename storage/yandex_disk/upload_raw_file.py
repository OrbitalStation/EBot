from yadisk.exceptions import ForbiddenError, ParentNotFoundError
from storage.yandex_disk.service import get_yadisk
from properties import const


def upload_raw_file(bot, message, filepath, title) -> str | None:
    if (yyy := get_yadisk(bot, message)) is None:
        return
    yandex_disk, yy = yyy
    bot.send_message(message.chat.id, const("YDFileUploadStart"))
    try:
        yy.upload(filepath, "/" + yandex_disk.folder_name.value + "/" + title)
    except ForbiddenError as err:
        bot.send_message(message.chat.id, const("YDForbidden") % (const("YDPermissionWrite"), str(err)))
        return
    except ParentNotFoundError as err:
        bot.send_message(message.chat.id,
                         const("YDFileParentNotFoundError") % str(yandex_disk.folder_name.value) + ' ' + str(err))
        return
    bot.send_message(message.chat.id, const("FileUploadSuccess"))
    return const("yandexDiskPrefix") + yandex_disk.folder_name.value + const("yandexDiskFileURLContinuation")\
        + yandex_disk.folder_name.value + '%2F' + title
