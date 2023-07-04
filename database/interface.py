from dataclasses import dataclass
from storage.configurable import configurable
from storage.google_drive.setcredentials import set_credentials
from storage.google_drive.setfolderid import setfolderid


@dataclass(frozen=True)
@configurable
class Credentials:
    value: str
    __on_set__ = set_credentials


@dataclass(frozen=True)
@configurable
class FolderID:
    value: str

    @staticmethod
    def __on_set__(bot, message, _):
        setfolderid(bot, message)


@dataclass(frozen=True)
@configurable
class GoogleDrive:
    credentials: Credentials
    folder_id: FolderID


@dataclass(frozen=True)
@configurable
class CloudStorage:
    google_drive: GoogleDrive
    # Name of the preferred cloud storage
    preferred: str


@dataclass(frozen=True)
@configurable
class User:
    # Primary key
    uid: int
    email: str
    storage: CloudStorage


class Database:
    @staticmethod
    def update_user(uid: int, **fields):
        raise NotImplementedError

    @staticmethod
    def fetch_user(uid: int) -> User:
        raise NotImplementedError
