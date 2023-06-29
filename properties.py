from os import listdir


_props = {}


def load_properties(dirpath: str, sep: str = '=', comment_char: str = '#'):
    """
    Read the file passed as parameter as a properties file.
    """
    global _props

    for filepath in listdir(dirpath):
        if not filepath.endswith('.properties'):
            continue
        file = concat_strings(dirpath + '/' + filepath)
        for line in file.split("\n"):
            line = line.strip()
            if line and not line.startswith(comment_char):
                key_value = line.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"').strip("'")
                _props[key] = value


def concat_strings(filepath: str) -> str:
    with open(filepath, "rt") as file:
        return file.read().replace('\\\n', ' ')


def const(name: str) -> str:
    return _props[name]
