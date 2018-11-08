import datetime
import sqlite3
import time
import typing
import urllib.parse
from os import makedirs
from os import path

from dateutil import tz
from meerk.calendar import IcsCalendar
from meerk.intervals import SimpleCalEventsIntervals
from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects.sqlite import compile

from .FileTimeIntervals import FileTimeIntervals
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

    def sync(self, folder: str) -> None:
        with sqlite3.connect(self.db_name) as connection:
            row = connection.execute(
                *compile(
                    Q(T.icalendar).fields('*').where(
                        T.icalendar.user == self.user and
                        T.icalendar.url == self.url
                    )
                )
            ).fetchone()
            url = row[1]

            sync_dir = path.join(folder, self.user, 'ics')
            if not path.exists(sync_dir):
                makedirs(sync_dir)

            IcsCalendar(
                url,
                SimpleCalEventsIntervals(
                    tz.tzlocal(),
                    FileTimeIntervals(path.join(sync_dir, urllib.parse.quote(self.url, safe='')))
                )
            ).sync()

            connection.execute(
                *Q(
                    T.icalendar, result=Result(compile=compile)
                ).where(
                    T.icalendar.user == self.user and
                    T.icalendar.url == self.url
                ).update({
                    T.icalendar.sync_time: int(round(time.time() * 1000))
                })
            )
