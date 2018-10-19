import abc


class Users:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add(self, email):
        # type: (str) -> None
        pass

    @abc.abstractmethod
    def contains(self, email):
        # type: (str) -> bool
        pass
