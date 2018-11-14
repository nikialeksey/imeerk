import abc


class Periodic(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self) -> None:
        pass
