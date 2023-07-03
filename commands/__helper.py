from properties import const
from database import SQLiteDB as DB


def getter(field: str, name_key: str):
    def inner(bot, message):
        name = const(name_key)
        DB.create_table_if_not_exists()
        user = DB.create_user_if_not_exists(message.from_user.id)
        value = getattr(user, field)
        if value == "":
            bot.send_message(message.chat.id, const('botUserGetterHasNoPropertyCmd') % name)
        else:
            bot.send_message(message.chat.id, const('botUserGetterHasPropertyCmd') % name + ' ' + value)

    return inner


def user_answered(bot, update, message, name):
    def hdl(answer):
        if answer.content_type == "text":
            if answer.text is None or answer.text == "":
                bot.send_message(message.chat.id, const("botUserSetterNoArgErrorCmd") % name)
                return
            answer.text = answer.text.strip()
            if answer.text.startswith('/'):
                from commands import execute_command
                execute_command(bot, answer)
                return
        elif answer.content_type == "photo":
            bot.send_message(message.chat.id, const("botUserSetterNoArgErrorCmd") % name)
            return
        elif answer.content_type == "document":
            pass
        update(answer)

    return hdl


def update_single_field(bot, message, value, field_name, field_human_name):
    if (updated := DB.update_user(message.from_user.id, **{field_name: value})) is None:
        #TODO send_message
        bot.send_message(message.chat.id, "//MAKE ERROR TEXT PLEASE//")
        return
    bot.send_message(message.chat.id, const("botUserSetterSuccessCmd") % field_human_name + ' ' + value)


def setter(field: str, name_key: str, *, extra_info: str | None = None, update_decorator=None):
    def inner(bot, message):
        def update(answer):
            if answer.content_type == "text":
                update_single_field(bot, answer, answer.text, field, name)

        if update_decorator is not None:
            update = update_decorator(update)

        name = const(name_key)
        DB.create_table_if_not_exists()
        DB.create_user_if_not_exists(message.from_user.id, do_fetch=False)

        message = bot.send_message(message.chat.id, const("botUserSetterAskCmd") % name)

        if extra_info is not None:
            message = bot.send_message(message.chat.id, const(extra_info))

        bot.register_next_step_handler(message, user_answered(bot, update, message, name))
    return inner


def send_markdown(bot, message, path):
    with open(path, "rb") as file:
        msg = file.read().decode("utf-8")
    return bot.send_message(message.chat.id, msg, parse_mode="Markdown")
