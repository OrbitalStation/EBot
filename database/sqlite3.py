from properties import const
from sqlite3 import Cursor
from database.interface import Database, User
import sqlite3


class SQLiteDB(Database):
    pyTy2sqlTy = {
        'int': 'INT',
        'str': 'TEXT'
    }

    @staticmethod
    def create_table_if_not_exists():
        fields = ', '.join([f'{field} {SQLiteDB.pyTy2sqlTy[value.__name__]}{" PRIMARY KEY" if field == "uid" else ""}'
                            for field, value in SQLiteDB.ufields.items()])
        SQLiteDB._mutate(f"CREATE TABLE IF NOT EXISTS {const('dbTableName')}({fields});")

    @staticmethod
    def create_user_if_not_exists(uid: int, do_fetch: bool = True) -> User | None:
        if (fetched := SQLiteDB.fetch_user(uid)) is None:
            fields, values = zip(*[(field, ty()) for field, ty in SQLiteDB.ufields.items() if field != 'uid'])
            placeholders = ('?,' * len(SQLiteDB.ufields))[:-1]
            SQLiteDB._mutate(f"INSERT INTO {const('dbTableName')} (uid, {', '.join(fields)}) VALUES({placeholders});",
                             (uid, *values))
            if do_fetch:
                return SQLiteDB.fetch_user(uid)
        if do_fetch:
            return fetched

    @staticmethod
    def update_user(uid: int, do_fetch: bool = True, **kwargs) -> User | None:
        update = ", ".join([(field + ' = ' + '"' + value.replace('"', '""') + '"') for field, value in kwargs.items()])
        SQLiteDB._mutate(f'UPDATE {const("dbTableName")} SET {update} WHERE uid = ?', (uid,))
        if do_fetch:
            return SQLiteDB.fetch_user(uid)

    @staticmethod
    def fetch_user(uid: int) -> User | None:
        if (fetched := SQLiteDB._fetch(f"SELECT * FROM {const('dbTableName')} WHERE uid=?", (uid,)).fetchone()) is None:
            return
        return User(*fetched)

    @staticmethod
    def _mutate(request: str, *args, **kwargs):
        con = sqlite3.connect(const("dbPath"))
        cur = con.cursor()
        cur.execute(request, *args, **kwargs)
        con.commit()
        cur.close()

    @staticmethod
    def _fetch(request: str, *args, **kwargs) -> Cursor:
        con = sqlite3.connect(const("dbPath"))
        cur = con.cursor()
        return cur.execute(request, *args, **kwargs)
