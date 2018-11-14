from .CalendarsPeriodic import CalendarsPeriodic
from .GroupPeriodic import GroupPeriodic
from .NotificationsPeriodic import NotificationsPeriodic
from .Periodic import Periodic


class ImeerkPeriodic(Periodic):

    def __init__(self):
        self.group = GroupPeriodic(
            [
                CalendarsPeriodic(),
                NotificationsPeriodic()
            ]
        )

    def run(self) -> None:
        self.group.run()
