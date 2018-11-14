from celery import current_app
from celery.bin import worker

from .Periodic import Periodic


class CalendarsPeriodic(Periodic):
    def run(self) -> None:
        worker.worker(app=current_app).run(
            broker='pyamqp://guest@localhost//',
            loglevel='INFO',
            traceback=True
        )
        # @todo #13:30m Add calendars syncing celery task
