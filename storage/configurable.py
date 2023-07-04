from button import markup
from properties import const


def configurable(cls):
    def _buttons():
        for field, ty in cls.__annotations__.items():
            if 'configure' in ty.__dict__:
                yield ty.__name__
            else:
                yield field

    def _leaf(bot, path):
        from commands.__helper import user_answered, update_single_field

        def hdl(answer):
            if answer.content_type == "text":
                update_single_field(bot, answer, answer.text, '_'.join(path), path[-1])

        def inner(bot2, message, answer):
            if answer == 'Yes':
                if hasattr(cls, '__on_set__'):
                    cls.__on_set__(bot, message, path)
                else:
                    message = bot2.send_message(message.chat.id, const("botUserSetterAskCmd") % path[-1])
                    bot2.register_next_step_handler(message, user_answered(bot2, hdl, message, path[-1]))
            elif answer == 'No':
                bot2.send_message(message.chat.id, const("botLeavingAsItIs"))
        return inner

    def _con(path):
        def inner(bot, message, chosen):
            for field, ty in cls.__annotations__.items():
                if ty.__name__ == chosen:
                    path.append(field)
                    ty.configure(bot, message, path=path)
                    break
                elif field == chosen:
                    from database import db
                    path.append(field)
                    fd = db.fetch_user(message.from_user.id)
                    for part in path:
                        fd = getattr(fd, part)
                    key = "botUserGetterHasPropertyCmd" if fd != "" else "botUserGetterHasNoPropertyCmd"
                    bot.send_message(message.chat.id, const(key) % field + ' ' + str(fd))
                    bot.send_message(
                        message.chat.id,
                        const("botConfigureDoChangeCmd"),
                        reply_markup=markup(bot, message, _leaf(bot, path), ['Yes', 'No']))
                    break
        return inner

    def config(bot, message, path):
        if len(cls.__annotations__) > 1:
            bot.send_message(
                message.chat.id,
                const("botConfigurePleaseChooseCmd"),
                reply_markup=markup(bot, message, _con(path), _buttons()))
        else:
            _con(path)(bot, message, tuple(_buttons())[0])

    cls.configure = config
    return cls
