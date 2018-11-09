import sqlite3

from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects.sqlite import compile

from .SlackNotifications import SlackNotifications


class DbSlackNotifications(SlackNotifications):

    def __init__(self, db_name: str, user: str) -> None:
        self.db_name = db_name
        self.user = user

    def add(self, team: str, token: str, profile: str) -> None:
        with sqlite3.connect(self.db_name) as connection:
            connection.execute(
                *Q(
                    T.slack, result=Result(compile=compile)
                ).insert(
                    {
                        T.slack.user: self.user,
                        T.slack.team: team,
                        T.slack.token: token,
                        T.slack.profile: profile,
                        T.slack.busy_text: '',
                        T.slack.busy_emoji: '',
                        T.slack.available_text: '',
                        T.slack.available_emoji: '',
                    }
                )
            )

    def as_html(self) -> str:
        result = ''
        with sqlite3.connect(self.db_name) as connection:
            rows = connection.execute(
                *compile(
                    Q(T.slack).fields('*').where(T.slack.user == self.user)
                )
            ).fetchall()

            for row in rows:
                # user = row[0]
                team = row[1]
                # token = row[2]
                # profile = row[3]
                # busy_text = row[4]
                # busy_emoji = row[5]
                # available_text = row[6]
                # available_emoji = row[7]

                result += f'<li><strong>Slack:</strong> <code>{team}</code></li>\n'

        return f'<ul>\n{result}</ul>'
