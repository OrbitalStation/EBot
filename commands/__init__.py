from iterate_through_modules_in_cwd import iterate


_commands = {}


@iterate(__file__)
def _cb(path, mod):
    _commands[path] = mod.command


def register_all_commands(bot):
    def handler(cmd):
        def hd(message):
            return _commands[cmd](bot, message)
        return hd

    for command in _commands.keys():
        bot.message_handler(commands=[command])(handler(command))
