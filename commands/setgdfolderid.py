from commands.__helper import setter


def _folder_id_wrap(_update):
    def inner(answer):
        if not check_is_folder_id(answer.text):
            answer.text = get_folder_id_from_link(answer.text)
        _update(answer)
    return inner


command = setter(
    "google_disk_folder_id",
    "botHumanGDFolderID",
    extra_info="botSetGDFolderIDExtraInfoCmd",
    update_decorator=_folder_id_wrap
)


def check_is_folder_id(string):
    return string.find('/') == -1 and string.find('.') == -1


def get_folder_id_from_link(link: str):
    return link[link.rfind('/') + 1:link.find('?')]
