import abc


class SlackChats(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add(self, team, token, profile):
        # type: (str, str, str) -> None
        pass
