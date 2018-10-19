import abc

from imeerk.calendars.icalendar import IcalCalendars
from imeerk.chats.slack import SlackChats


class User:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calendars(self):
        # type: () -> IcalCalendars
        ...

    @abc.abstractmethod
    def chats(self):
        # type: () -> SlackChats
        ...

    @abc.abstractmethod
    def url(self) -> str:
        ...
