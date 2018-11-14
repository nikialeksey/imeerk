import abc


class SlackNotification(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update_busy(self, busy_text: str, busy_emoji: str) -> None:
        pass

    @abc.abstractmethod
    def update_available(self, available_text: str, available_emoji: str) -> None:
        pass
