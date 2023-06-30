from properties import const
from sqlite3 import Cursor
from dataclasses import dataclass
import sqlite3

pyTy2sqlTy = {
    'int': 'INT',
    'str': 'TEXT'
}


@dataclass(frozen=True)
class User:
    # Primary key
    uid: int
    email: str
    google_disk_credentials: str


ufields = User.__dict__['__annotations__']


def create_table_if_not_exists():
    fields = ', '.join([f'{field} {pyTy2sqlTy[value.__name__]}{" PRIMARY KEY" if field == "uid" else ""}'
                        for field, value in ufields.items()])
    _mutate(f"CREATE TABLE IF NOT EXISTS {const('dbTableName')}({fields});")


def create_user_if_not_exists_and_fetch_if_needed(uid: int, do_fetch: bool) -> User:
    if (fetched := fetch_user(uid)) is None:
        fields, values = zip(*[(field, ty()) for field, ty in ufields.items() if field != 'uid'])
        placeholders = ('?,' * len(ufields))[:-1]
        _mutate(f"INSERT INTO {const('dbTableName')} (uid, {', '.join(fields)}) VALUES({placeholders});",
                (uid, *values))
        if do_fetch:
            return fetch_user(uid)
    if do_fetch:
        return fetched


def update_user(uid: int, **kwargs):
    update = ", ".join([(field + ' = ' + '"' + value.replace('"', '""') + '"') for field, value in kwargs.items()])
    _mutate(f'UPDATE {const("dbTableName")} SET {update} WHERE uid = ?', (uid,))


def fetch_user(uid: int) -> User | None:
    if (fetched := _fetch(f"SELECT * FROM {const('dbTableName')} WHERE uid=?", (uid,)).fetchone()) is None:
        return
    return User(*fetched)


def _mutate(request: str, *args, **kwargs):
    con = sqlite3.connect(const("dbPath"))
    cur = con.cursor()
    cur.execute(request, *args, **kwargs)
    con.commit()
    cur.close()


def _fetch(request: str, *args, **kwargs) -> Cursor:
    con = sqlite3.connect(const("dbPath"))
    cur = con.cursor()
    return cur.execute(request, *args, **kwargs)
