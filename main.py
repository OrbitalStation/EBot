from init import init
from commands import register_all_commands
from listeners import register_all_listeners


bot = init('assets/properties')
register_all_commands(bot)
register_all_listeners(bot)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
