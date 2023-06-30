from commands.__helper import send_markdown
from properties import const


# TODO getting GD botfolder link
def command(bot, message):
    attachment = const("googleCloudAccountGuidePath")
    send_markdown(bot, message, attachment)
