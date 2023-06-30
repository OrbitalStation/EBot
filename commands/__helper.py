import telebot

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


def user_answered(bot, update, message, validate, name):
    def hdl(answer):
        if answer.content_type == "text":
            if answer.text is None or answer.text == "":
                bot.send_message(message.chat.id, const("botUserSetterNoArgErrorCmd") % name)
                return
            answer.text = answer.text.strip()
            if validate is not None:
                if not validate(answer.text):
                    return
        elif answer.content_type == "photo":
            bot.send_message(message.chat.id, const("botUserSetterNoArgErrorCmd") % name)
            return
        elif answer.content_type == "document":
            pass
        update(answer)

    return hdl


def update_single_field(bot, message, value, field_name, field_human_name):
    bot.send_message(message.chat.id, const("botUserSetterSuccessCmd") % field_human_name + ' ' + value)
    db.update_user(message.from_user.id, **{field_name: value})


def setter(
        field: str,
        name_key: str,
        *,
        extra_info_key: str | None = None,
        md_attachment_path: str | None = None
):
    def inner_decorator(validate):
        def inner(bot, message):
            def update(answer):
                if answer.content_type == "text":
                    update_single_field(bot, answer, answer.text, field, name)
                elif answer.content_type == "document":
                    doc = answer.document
                    file_info = bot.get_file(doc.file_id)
                    file_bytes = bot.download_file(file_info.file_path)
                    update_single_field(bot, answer, file_bytes.decode("utf-8"), field, name)
                else:
                    pass

            name = const(name_key)
            db.create_table_if_not_exists()
            db.create_user_if_not_exists_and_fetch_if_needed(message.from_user.id, do_fetch=False)

            message = bot.send_message(message.chat.id, const("botUserSetterAskCmd") % name)
            if extra_info_key is not None:
                message = bot.send_message(message.chat.id, const(extra_info_key))
            if md_attachment_path is not None:
                attachment = const(md_attachment_path)
                with open(attachment, "rb") as file:
                    msg = file.read().decode("utf-8")
                    message = bot.send_message(message.chat.id, msg, parse_mode="Markdown")
            bot.register_next_step_handler(message, user_answered(bot, update, message, validate, name))

        return inner

    return inner_decorator
