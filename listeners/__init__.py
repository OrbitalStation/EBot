from iterate_through_modules_in_cwd import iterate


_listeners = {}


@iterate(__file__)
def _cb(path, mod):
    _listeners[path] = mod.listener


def register_all_listeners(bot):
    def handler(lis):
        def hd(message):
            return _listeners[lis](bot, message)
        return hd

    for lisne in _listeners.keys():
        bot.message_handler(content_types=[lisne])(handler(lisne))
