from commands.__helper import send_markdown
from properties import const


# TODO getting GD botfolder link
def command(bot, message):
    send_markdown(bot, message, const("googleCloudAccountGuidePath"))
