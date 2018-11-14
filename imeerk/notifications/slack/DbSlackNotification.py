import sqlite3

from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects.sqlite import compile

from .SlackNotification import SlackNotification


class DbSlackNotification(SlackNotification):

    def __init__(self, db_name, user, token) -> None:
        self.db_name = db_name
        self.user = user
        self.token = token

    def update_busy(self, busy_text: str, busy_emoji: str) -> None:
        with sqlite3.connect(self.db_name) as connection:
            connection.execute(
                *Q(
                    T.slack, result=Result(compile=compile)
                ).where(
                    T.slack.user == self.user and
                    T.slack.token == self.token
                ).update({
                    T.slack.busy_text: busy_text,
                    T.slack.busy_emoji: busy_emoji,
                })
            )

    def update_available(self, available_text: str, available_emoji: str) -> None:
        with sqlite3.connect(self.db_name) as connection:
            connection.execute(
                *Q(
                    T.slack, result=Result(compile=compile)
                ).where(
                    T.slack.user == self.user and
                    T.slack.token == self.token
                ).update({
                    T.slack.available_text: available_text,
                    T.slack.available_emoji: available_emoji,
                })
            )
