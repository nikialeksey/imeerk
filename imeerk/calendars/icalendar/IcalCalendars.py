import abc
import typing

from .IcalCalendar import IcalCalendar


class IcalCalendars:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add(self, url, name):
        # type: (str, str) -> None
        pass

    @abc.abstractmethod
    def calendar(self, url: str) -> IcalCalendar:
        pass

    @abc.abstractmethod
    def as_html(self, url: typing.Callable[[str], str]) -> str:
        pass
