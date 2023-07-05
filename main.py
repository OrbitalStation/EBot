from init import init
from commands import register_all_commands
from listeners import register_all_listeners


if __name__ == '__main__':
    bot = init(properties_dir='assets/properties')
    register_all_commands(bot)
    register_all_listeners(bot)
    bot.infinity_polling(timeout=40)
