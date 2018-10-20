import abc

from imeerk.calendars.icalendar import IcalCalendars
from imeerk.chats.slack import SlackChats


class User:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calendars(self) -> IcalCalendars:
        pass

    @abc.abstractmethod
    def chats(self) -> SlackChats:
        pass

    @abc.abstractmethod
    def url(self) -> str:
        pass
