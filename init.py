from properties import load_properties, const
from telebot import TeleBot


def init(properties_dir: str) -> TeleBot:
    load_properties(properties_dir)

    telebot = TeleBot(const("telebotToken"))

    return telebot
