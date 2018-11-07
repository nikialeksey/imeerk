import datetime
import sqlite3
import typing

from sqlbuilder.smartsql import Q, T
from sqlbuilder.smartsql.dialects.sqlite import compile

from .IcalCalendar import IcalCalendar


class DbIcalCalendar(IcalCalendar):

    def __init__(self, db_name: str, user: str, url: str) -> None:
        self.db_name = db_name
        self.user = user
        self.url = url

    def as_html(self, sync_url: typing.Callable[[str], str]) -> str:
        result = ''
        with sqlite3.connect(self.db_name) as connection:
            row = connection.execute(
                *compile(
                    Q(T.icalendar).fields('*').where(
                        T.icalendar.user == self.user and
                        T.icalendar.url == self.url
                    )
                )
            ).fetchone()
            try:
                sync = datetime.datetime.fromtimestamp(row[3] / 1000)
            except OSError:
                sync = datetime.datetime.min
            name = row[2]
            url = row[1]

            delta: datetime.timedelta = datetime.datetime.now() - sync

            if delta.seconds > 60:
                sync_html = f'<mark>Sync was at {str(sync)}</mark>'
            else:
                sync_html = f'<code>Sync was at {str(sync)}</code>'
            result = f'''
                <h2>{name}</h2>
                <span><strong>Url: </strong>{url}</span></br>
                {sync_html}</br>
                <span><a href="{sync_url(url)}">Sync it now!</a></span></br>
            '''

        return result

    def sync(self) -> None:
        # @todo #5:30m Add sync calendar into user cash
        pass
