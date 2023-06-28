import sqlite3


def get_user_email(user_id):
    con = sqlite3.connect('assets/users.db')
    cur = con.cursor()
    email = cur.execute('SELECT email FROM users WHERE user_id=?', (user_id,)).fetchone()
    cur.close()
    return email[0]
