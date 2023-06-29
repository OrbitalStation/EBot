from properties import const
import database as db


def getter(field: str, name_key: str):
    def inner(bot, message):
        name = const(name_key)
        db.create_table_if_not_exists()
        user = db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=True)
        value = getattr(user, field)
        if value == "":
            bot.send_message(message.chat.id, const('botUserGetterHasNoPropertyCmd') % name)
        else:
            bot.send_message(message.chat.id, const('botUserGetterHasPropertyCmd') % name + ' ' + value)
    return inner


def setter(field: str, name_key: str, *, extra_info_key: str | None = None):
    def inner_decorator(validate):
        def inner(bot, message):
            def user_answered(answer):
                if answer.text is None or answer.text == "":
                    bot.send_message(message.chat.id, const("botUserSetterNoArgErrorCmd") % name)
                    return
                answer.text = answer.text.replace('"', '\\"')
                if not validate(answer.text):
                    return
                db.update_user(message.from_user.id, **{field: f'"{answer.text}"'})
                bot.send_message(message.chat.id, const("botUserSetterSuccessCmd") % name + ' ' + answer.text)

            name = const(name_key)
            db.create_table_if_not_exists()
            db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=False)

            message = bot.send_message(message.chat.id, const("botUserSetterAskCmd") % name)
            if extra_info_key is not None:
                message = bot.send_message(message.chat.id, const(extra_info_key))
            bot.register_next_step_handler(message, user_answered)
        return inner
    return inner_decorator
