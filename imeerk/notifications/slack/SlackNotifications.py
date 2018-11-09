import abc


class SlackNotifications(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add(self, team, token, profile):
        # type: (str, str, str) -> None
        pass

    @abc.abstractmethod
    def as_html(self) -> str:
        pass
