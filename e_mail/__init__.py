__all__ = ['send_raw', 'send', 'create_title_for_email_and_attachment']

from convert_time_from_unix import convert


def create_title_for_email_and_attachment(time: str):
    return "Сообщение из Телеграмма, " + time
