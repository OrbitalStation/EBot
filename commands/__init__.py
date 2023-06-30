from iterate_through_modules_in_cwd import iterate
from properties import const

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


def execute_command(bot, message):
    if not message.text.startswith('/'):
        return
    try:
        _commands[message.text[len('/'):]](bot, message)
    except KeyError:
        handle_unknown_command(bot, message)


def handle_unknown_command(bot, message):
    bot.send_message(message.chat.id, const("botUnknownCmdError"))
