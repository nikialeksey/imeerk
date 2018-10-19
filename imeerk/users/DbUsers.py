import sqlite3
from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects.sqlite import compile
from .Users import Users


class DbUsers(Users):

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name

    def add(self, email):
        # type: (str) -> None
        with sqlite3.connect(self.db_name) as connection:
            connection.execute(
                *Q(
                    T.user, result=Result(compile=compile)
                ).insert(
                    {
                        T.user.email: email
                    }
                )
            )

    def contains(self, email):
        # type: (str) -> bool
        contains = False
        with sqlite3.connect(self.db_name) as connection:
            info = connection.execute(
                *compile(Q(T.user).fields('*').where(T.user.email == email))
            ).fetchone()
            if info:
                contains = True
        return contains
