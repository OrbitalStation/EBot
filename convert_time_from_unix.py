import time


def convert(unix: int):
    return time.strftime("%d.%M.%Y %H:%M:%S", time.localtime(unix))
