import time


def convert(unix: int):
    return time.strftime("%H:%M:%S %Y-%m-%d", time.localtime(unix))
