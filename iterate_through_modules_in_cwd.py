from importlib import import_module
from os import listdir
from pathlib import Path


def iterate(file):
    def inner(cb):
        cwd = Path(file).parent.resolve()

        for path in listdir(cwd):
            if path.startswith("__") or path.startswith("."):
                continue
            path = path[:path.rfind(".")]
            cb(path, import_module('.' + path, package=cwd.stem))
    return inner
