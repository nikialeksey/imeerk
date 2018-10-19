import abc


class Migration:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def apply(self):
        # type: () -> None
        pass
