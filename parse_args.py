MSG_SEP = ' '


def parse(message: str) -> str | None:
    if (pos := message.find(MSG_SEP)) == -1:
        return
    return message[pos + len(MSG_SEP):].strip()
