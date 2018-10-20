import sqlite3
from sqlite3.dbapi2 import Connection
from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects.sqlite import compile


class DbVersion:

    def __init__(self, db_name: str, table: str = 'version') -> None:
        self.db_name = db_name
        self.table = table

    def number(self):
        with sqlite3.connect(self.db_name) as connection:
            self.__ensure_table(connection)
            version = connection.execute(
                *compile(Q(T(self.table)).fields('number'))
            ).fetchone()[0]

        return version

    def update(self, number: int) -> None:
        with sqlite3.connect(self.db_name) as connection:
            self.__ensure_table(connection)
            connection.execute(
                *Q(T(self.table), result=Result(compile=compile)).update(
                    {
                        T(self.table).number: number
                    }
                )
            )

    def __ensure_table(self, connection: Connection) -> None:
        info = connection.execute(
            *compile(
                Q(T.sqlite_master)
                .fields('*')
                .where((T.sqlite_master.name == 'version') & (T.sqlite_master.type == 'table'))
            )
        ).fetchone()

        if not info:
            connection.execute('CREATE TABLE version (number INTEGER NOT NULL)')
            connection.execute(
                *Q(T(self.table), result=Result(compile=compile)).insert({T(self.table).number: 0})
            )
