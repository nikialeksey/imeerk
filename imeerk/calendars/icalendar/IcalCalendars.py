import abc


class IcalCalendars:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add(self, url, name):
        # type: (str, str) -> None
        pass

    @abc.abstractmethod
    def as_html(self):
        # type: () -> str
        pass
