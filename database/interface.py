from dataclasses import dataclass


@dataclass(frozen=True)
class GoogleDrive:
    credentials: str
    folder_id: str


@dataclass(frozen=True)
class CloudStorage:
    google_drive: GoogleDrive
    # Name of the preferred cloud storage
    preferred: str


@dataclass(frozen=True)
class User:
    # Primary key
    uid: int
    email: str
    storage: CloudStorage


class Database:
    @staticmethod
    def create_table_if_not_exists():
        raise NotImplementedError

    @staticmethod
    def create_user_if_not_exists(uid: int, do_fetch: bool = True) -> User | None:
        raise NotImplementedError

    @staticmethod
    def update_user(uid: int, do_fetch: bool = True, **kwargs) -> User | None:
        raise NotImplementedError

    @staticmethod
    def fetch_user(uid: int) -> User | None:
        raise NotImplementedError

    @staticmethod
    def _mutate(request: str, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def _fetch(request: str, *args, **kwargs):
        raise NotImplementedError
