from listeners.__helper import listener
from properties import const
from e_mail.send import send
import database as db


@listener
def listener(bot, message):
    print('pikcha')
