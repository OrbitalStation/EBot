import time


def convert(unix: int):
    return time.strftime("%Y-%m-%d% %H:%M:%S", time.localtime(unix))
