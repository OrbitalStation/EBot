from properties import const
from sqlite3 import Cursor
from database.interface import Database, User
import sqlite3

CREATE_TABLE_SQL: str | None = None
CREATE_USER_SQL: tuple[str, tuple] | None = None

PY2SQL = {
    'int': 'INT',
    'str': 'TEXT'
}


def _unfold_annotations(field: str, ty: type) -> dict[str, type]:
    if PY2SQL.get(ty.__name__) is not None:
        return {field: ty}
    if field != "":
        field += '_'
    result = {}
    for subfield, subty in ty.__annotations__.items():
        result.update(_unfold_annotations(field + subfield, subty))
    return result


def _dataclass_from_sql(dataclass: type, sql: list):
    result = []
    for field, ty in dataclass.__annotations__.items():
        if PY2SQL.get(ty.__name__) is not None:
            result.append(sql.pop())
            continue
        result.append(_dataclass_from_sql(ty, sql))
    return dataclass(*result)


UFIELDS = _unfold_annotations("", User)


class SQLiteDB(Database):
    @staticmethod
    def create_table_if_not_exists():
        global CREATE_TABLE_SQL
        if CREATE_TABLE_SQL is None:
            fields = ', '.join(
                [f'{field} {PY2SQL[value.__name__]}{" PRIMARY KEY" if field == "uid" else ""}'
                 for field, value in UFIELDS.items()])
            CREATE_TABLE_SQL = f"CREATE TABLE IF NOT EXISTS {const('dbTableName')}({fields});"
        SQLiteDB._mutate(CREATE_TABLE_SQL)

    @staticmethod
    def create_user(uid: int):
        global CREATE_USER_SQL

        if CREATE_USER_SQL is None:
            fields, values = zip(*[(field, ty()) for field, ty in UFIELDS.items() if field != 'uid'])
            placeholders = ('?,' * len(UFIELDS))[:-1]
            CREATE_USER_SQL = f"INSERT INTO {const('dbTableName')}" \
                              f" (uid, {', '.join(fields)}) VALUES({placeholders});", values
        SQLiteDB._mutate(CREATE_USER_SQL[0], (uid, *CREATE_USER_SQL[1]))

    @staticmethod
    def update_user(uid: int, **kwargs):
        if SQLiteDB.fetch_user_or(uid) is None:
            SQLiteDB.create_user(uid)
        update = ", ".join([(field + ' = ' + '"' + value.replace('"', '""') + '"') for field, value in kwargs.items()])
        SQLiteDB._mutate(f'UPDATE {const("dbTableName")} SET {update} WHERE uid = ?', (uid,))

    @staticmethod
    def fetch_user(uid: int) -> User:
        if (fetched := SQLiteDB.fetch_user_or(uid)) is None:
            SQLiteDB.create_user(uid)
            fetched = SQLiteDB.fetch_user_or(uid)
        return fetched

    @staticmethod
    def fetch_user_or(uid: int) -> User | None:
        SQLiteDB.create_table_if_not_exists()
        if (fetched := SQLiteDB._fetch(f"SELECT * FROM {const('dbTableName')} WHERE uid=?", (uid,)).fetchone()) is None:
            return
        return _dataclass_from_sql(User, list(fetched)[::-1])

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
