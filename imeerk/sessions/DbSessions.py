import sqlite3
import uuid

from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects.sqlite import compile

from imeerk.users import DbUser
from imeerk.users import User
from .Sessions import Sessions


class DbSessions(Sessions):

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name

    def user(self, token: str) -> User:
        user = ''
        with sqlite3.connect(self.db_name) as connection:
            row = connection.execute(
                *compile(
                    Q(T.session).fields('user').where(T.session.token == token)
                )
            ).fetchone()
            user = row[0]
        return DbUser(self.db_name, user)

    def add(self, user: str) -> str:
        token = str(uuid.uuid4())
        with sqlite3.connect(self.db_name) as connection:
            connection.execute(
                *Q(
                    T.session, result=Result(compile=compile)
                ).insert(
                    {
                        T.session.user: user,
                        T.session.token: token
                    }
                )
            )
        return token
