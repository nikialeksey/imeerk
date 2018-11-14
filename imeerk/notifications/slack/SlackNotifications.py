import abc

from .SlackNotification import SlackNotification


class SlackNotifications(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add(self, team: str, token: str, profile: str) -> None:
        pass

    @abc.abstractmethod
    def notification(self, token: str) -> SlackNotification:
        pass

    @abc.abstractmethod
    def as_html(self) -> str:
        pass
