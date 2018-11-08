import abc
import typing


class IcalCalendar(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def as_html(self, sync_url: typing.Callable[[str], str]) -> str:
        pass

    @abc.abstractmethod
    def sync(self, folder: str) -> None:
        pass
