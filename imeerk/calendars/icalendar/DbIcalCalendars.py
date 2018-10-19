import sqlite3

from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects.sqlite import compile

from .IcalCalendars import IcalCalendars


class DbIcalCalendars(IcalCalendars):

    def __init__(self, db_name: str, user: str) -> None:
        self.db_name = db_name
        self.user = user

    def add(self, url, name):
        # type: (str, str) -> None
        with sqlite3.connect(self.db_name) as connection:
            connection.execute(
                *Q(
                    T.icalendar, result=Result(compile=compile)
                ).insert(
                    {
                        T.icalendar.user: self.user,
                        T.icalendar.url: url,
                        T.icalendar.name: name,
                        T.icalendar.sync_time: 0
                    }
                )
            )

    def as_html(self):
        # type: () -> str
        result = ''
        with sqlite3.connect(self.db_name) as connection:
            rows = connection.execute(
                *compile(
                    Q(T.icalendar).fields('*').where(T.icalendar.user == self.user)
                )
            ).fetchall()

            result = '<ul>{0}</ul>'.format(
                '\n'.join(
                    map(
                        lambda row: '<li><strong>{0}</strong>: <a href="{1}">{1}</a></li>'.format(
                            row[2], row[1]
                        ),
                        rows
                    )
                )
            )

        return result
