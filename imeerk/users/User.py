import abc

from imeerk.calendars.icalendar import IcalCalendars
from imeerk.notifications.slack import SlackNotifications


class User:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calendars(self) -> IcalCalendars:
        pass

    @abc.abstractmethod
    def notifications(self) -> SlackNotifications:
        pass

    @abc.abstractmethod
    def url(self) -> str:
        pass
