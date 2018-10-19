import sqlite3

from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects.sqlite import compile

from .SlackChats import SlackChats


class DbSlackChats(SlackChats):

    def __init__(self, db_name: str, user: str) -> None:
        self.db_name = db_name
        self.user = user

    def add(self, team, token, profile):
        # type: (str, str, str) -> None
        with sqlite3.connect(self.db_name) as connection:
            connection.execute(
                *Q(
                    T.slack, result=Result(compile=compile)
                ).insert(
                    {
                        T.slack.user: self.user,
                        T.slack.team: team,
                        T.slack.token: token,
                        T.slack.profile: profile
                    }
                )
            )
