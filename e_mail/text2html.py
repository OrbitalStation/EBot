from telebot.types import MessageEntity


# I(@orbitalstation) am not a creator nor an owner of this function
# I pay great respect to @sviat9440 and @badiboy for this excellent
#   solution and would like to clarify that this is the code from the
#   pyTelegramBotAPI python library.
# Thank you guys :)
def text2html(text: str, entities: list[MessageEntity] | None, custom_subs: dict[str, str] | None = None) -> str:
    """
    Author: @sviat9440 Updaters: @badiboy Message: "*Test* parse _formatting_, [url](https://example.com),
    [text_mention](tg://user?id=123456) and mention @username"

    .. code-block:: python3
        :caption: Example:

        message.html_text >> "<b>Test</b> parse <i>formatting</i>, <a href=\"https://example.com\">url</a>,
        <a href=\"tg://user?id=123456\">text_mention</a> and mention @username"

    Custom subs: You can customize the substitutes. By default, there is no substitute for the entities: hashtag,
    bot_command, email. You can add or modify substitute an existing entity. .. code-block:: python3 :caption: Example:

        message.custom_subs = {"bold": "<strong class=\"example\">{text}</strong>", "italic": "<i class=\"example\">{
        text}</i>", "mention": "<a href={url}>{text}</a>"} message.html_text >> "<strong
        class=\"example\">Test</strong> parse <i class=\"example\">formatting</i>,
        <a href=\"https://example.com\">url</a> and <a href=\"tg://user?id=123456\">text_mention</a> and mention <a
        href=\"https://t.me/username\">@username</a>"
    """

    if not entities:
        return text

    _subs = {
        "bold": "<b>{text}</b>",
        "italic": "<i>{text}</i>",
        "pre": "<pre>{text}</pre>",
        "code": "<code>{text}</code>",
        # "url": "<a href=\"{url}\">{text}</a>", # @badiboy plain URLs have no text and do not need tags
        "text_link": "<a href=\"{url}\">{text}</a>",
        "strikethrough": "<s>{text}</s>",
        "underline": "<u>{text}</u>",
        "spoiler": "<span class=\"tg-spoiler\">{text}</span>",
        "custom_emoji": "<tg-emoji emoji-id=\"{custom_emoji_id}\">{text}</tg-emoji>"
    }

    # @orbitalstation slight changes
    if custom_subs is not None:
        for key, value in custom_subs.items():
            _subs[key] = value
    utf16_text = text.encode("utf-16-le")
    html_text = ""

    def func(upd_text, subst_type=None, url=None, user=None, custom_emoji_id=None):
        upd_text = upd_text.decode("utf-16-le")
        if subst_type == "text_mention":
            subst_type = "text_link"
            url = "tg://user?id={0}".format(user.id)
        elif subst_type == "mention":
            url = "https://t.me/{0}".format(upd_text[1:])
        upd_text = upd_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if not subst_type or not _subs.get(subst_type):
            return upd_text
        subs = _subs.get(subst_type)
        if subst_type == "custom_emoji":
            return subs.format(text=upd_text, custom_emoji_id=custom_emoji_id)
        return subs.format(text=upd_text, url=url)

    offset = 0
    start_index = 0
    end_index = 0
    for entity in entities:
        if entity.offset > offset:
            # when the offset is not 0: for example, a __b__
            # we need to add the text before the entity to the html_text
            html_text += func(utf16_text[offset * 2: entity.offset * 2])
            offset = entity.offset

            new_string = func(utf16_text[offset * 2: (offset + entity.length) * 2], entity.type, entity.url,
                              entity.user, entity.custom_emoji_id)
            start_index = len(html_text)
            html_text += new_string
            offset += entity.length
            end_index = len(html_text)
        elif entity.offset == offset:
            new_string = func(utf16_text[offset * 2: (offset + entity.length) * 2], entity.type, entity.url,
                              entity.user, entity.custom_emoji_id)
            start_index = len(html_text)
            html_text += new_string
            end_index = len(html_text)
            offset += entity.length
        else:
            # Here we are processing nested entities. We shouldn't update offset, because they are the same as entity
            # before. And, here we are replacing previous string with a new html-rendered text(previous string is
            # already html-rendered, and we don't change it).
            entity_string = html_text[start_index: end_index].encode("utf-16-le")
            formatted_string = func(entity_string, entity.type, entity.url, entity.user,
                                    entity.custom_emoji_id).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;",
                                                                                                               ">")
            html_text = html_text[:start_index] + formatted_string + html_text[end_index:]
            end_index = len(html_text)

    if offset * 2 < len(utf16_text):
        html_text += func(utf16_text[offset * 2:])

    return html_text
