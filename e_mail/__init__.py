__all__ = ['send_raw', 'send', 'create_title_for_email']


def create_title_for_email(sender: str, time: str):
    return sender + " -- TG --" + time

