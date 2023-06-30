import time


def convert(unix: int):
    return time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(unix))
