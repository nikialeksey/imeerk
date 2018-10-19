import sqlite3

from .DbVersion import DbVersion
from .Migration import Migration


class MigrationInit(Migration):

    def __init__(self, db_name):
        # type: (str) -> None
        self.version = DbVersion(db_name)
        self.db_name = db_name

    def apply(self):
        # type: () -> None
        if self.version.number() == 0:
            with sqlite3.connect(self.db_name) as connection:
                connection.execute('PRAGMA foreign_keys = ON')
                connection.execute(
                    """
                    CREATE TABLE user (
                        email TEXT NOT NULL,
                        PRIMARY KEY(email)
                    )
                    """
                )
                connection.execute(
                    """
                    CREATE TABLE slack (
                        user TEXT NOT NULL,
                        team TEXT NOT NULL,
                        token TEXT NOT NULL,
                        profile TEXT NOT NULL,
                        PRIMARY KEY (user, team),
                        FOREIGN KEY (user) REFERENCES user (email) ON DELETE CASCADE
                    )
                    """
                )
                connection.execute(
                    """
                    CREATE TABLE icalendar (
                        user TEXT NOT NULL,
                        url TEXT NOT NULL,
                        name TEXT NOT NULL,
                        sync_time INTEGER NOT NULL,
                        PRIMARY KEY (user, url),
                        FOREIGN KEY (user) REFERENCES user (email) ON DELETE CASCADE
                    )
                    """
                )
                connection.execute(
                    """
                    CREATE TABLE session (
                        token TEXT NOT NULL,
                        user TEXT NOT NULL,
                        PRIMARY KEY (token),
                        FOREIGN KEY (user) REFERENCES user (email) ON DELETE CASCADE
                    )
                    """
                )

        self.version.update(1)
