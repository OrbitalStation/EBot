__all__ = ['send_raw', 'send', 'create_title_for_email_and_attachment']


def create_title_for_email_and_attachment(time: str):
    return "Сообщение из Телеграмма, " + time
