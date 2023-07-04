from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from copy import deepcopy


def _cb(bot, message, unique, callback):
    def inner(query):
        if not query.data.startswith(unique):
            print(bot.callback_query_handlers)
            return
        callback(bot, message, query.data[len(unique):])
        bot.callback_query_handlers.pop(0)
    return inner


def markup(bot, message, callback, buttons):
    unique = repr(callback)
    unique = unique[unique.find('0x'):unique.rfind('>')]
    kb = InlineKeyboardMarkup()
    for b in buttons:
        kb.add(InlineKeyboardButton(b, callback_data=unique + b))
    bot.callback_query_handler(func=lambda _: True)(_cb(bot, message, unique, callback))
    return kb
