import os
import sqlite3
from init import init
from get_email import get_user_email
from send_email import send_email
from google_disk import upload


bot = init('assets/properties/general.properties', 'assets/properties/sensitive.properties')

msg_id = 0
links = []

count = 0
media_id = 0
caption = ''


@bot.message_handler(content_types=['text', 'photo'])
def listener(message):
    con = sqlite3.connect('assets/users.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY, name TEXT, email TEXT, flag TEXT);""")
    con.commit()
    cur.close()

    insert_user_if_does_not_exist(message.from_user.id)

    if check_for_commands_and_handle_if_any(message):
        return

    email = get_user_email(message.from_user.id)
    if message.content_type == 'text':
        if message.forward_from or message.forward_from_chat:
            send_email(message, email, message.text, [])
            bot.send_message(message.from_user.id, "Письмо отправлено на почту ✅")

        else:
            bot.send_message(message.from_user.id, "Жду следующего сообщения...")

    elif message.content_type == 'photo':
        global count, media_id, caption

        if media_id == message.media_group_id:
            count += 1

        if message.media_group_id:
            media_id = message.media_group_id

        if message.caption:
            caption = message.caption

        file = bot.get_file(message.photo[-1].file_id)
        filename, file_exstension = os.path.splitext(file.file_path)

        downloaded_file = bot.download_file(file.file_path)
        src = 'files/' + str(message.photo[-1].file_id) + file_exstension

        with open(src, 'wb') as f:
            f.write(downloaded_file)

        link = upload(src, str(message.photo[-1].file_id) + file_exstension)

        if link:
            os.remove(src)
            links.append(link)
            bot.send_message(message.from_user.id, "Этот файл скачан на Google Drive\n\n"
                                                   f"Ссылка на файл: {link}")

        if len(links) == count:
            media_id = 0
            count = 0
            send_email(message, email, caption, links)

    else:
        bot.send_message(message.from_user.id, f"Тип файла: {message.content_type}")


def check_for_commands_and_handle_if_any(message):
    was_command = True
    if message.text == '/myEmailGet':
        email = get_user_email(message.from_user.id)
        if email is None:
            bot.send_message(message.chat.id, "Вы не указали электронную почту")
        else:
            bot.send_message(message.chat.id, "Ваша почта: " + email)
    elif message.text.startswith('/myEmailSet '):
        email = message.text[len('/myEmailSet '):].strip()
        set_email(message, email)
        bot.send_message(message.chat.id, "Ваша электронная почта: " + email)
    else:
        was_command = False
    return was_command


def user_exists(user_id):
    con = sqlite3.connect('assets/users.db')
    cur = con.cursor()
    return cur.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()


def set_email(message, email):
    user_id = message.from_user.id

    con = sqlite3.connect('assets/users.db')
    cur = con.cursor()

    insert = '''UPDATE users SET email = ? WHERE user_id = ?;'''
    data = (email, user_id)

    cur.execute(insert, data)
    con.commit()
    cur.close()


def insert_user_if_does_not_exist(user_id):
    if user_exists(user_id) is None:
        con = sqlite3.connect('assets/users.db')
        cur = con.cursor()

        insert = '''INSERT INTO users (user_id, flag) VALUES(?, ?);'''
        data = (user_id, 'name',)

        cur.execute(insert, data)
        con.commit()
        cur.close()


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
