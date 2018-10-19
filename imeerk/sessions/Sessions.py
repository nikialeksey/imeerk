import abc

from imeerk.users import User


class Sessions(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def user(self, token: str) -> User:
        pass

    @abc.abstractmethod
    def add(self, user: str) -> str:
        pass
