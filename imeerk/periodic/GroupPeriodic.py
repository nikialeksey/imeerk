import typing

from .Periodic import Periodic


class GroupPeriodic(Periodic):

    def __init__(self, periodics: typing.List[Periodic]) -> None:
        self.periodics = periodics

    def run(self) -> None:
        for periodic in self.periodics:
            periodic.run()
