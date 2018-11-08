import base64
import pickle
from datetime import datetime

from meerk.intervals.TimeIntervals import TimeIntervals


class FileTimeIntervals(TimeIntervals):

    def __init__(self, file: str) -> None:
        self.file = file

    def clear(self) -> None:
        open(self.file, 'w').close()

    def add(self, start: datetime, end: datetime, data: object) -> None:
        with open(self.file, 'a') as store:
            start_b64 = base64.b64encode(pickle.dumps(start)).decode('utf-8')
            end_b64 = base64.b64encode(pickle.dumps(end)).decode('utf-8')
            data_b64 = base64.b64encode(pickle.dumps(data)).decode('utf-8')
            store.write(f"{start_b64} {end_b64} {data_b64}\n")

    def is_inside(self, time: datetime) -> bool:
        is_inside = False
        with open(self.file) as store:
            for line in store:
                start_b64, end_b64, _ = line.split(' ')
                start: datetime = pickle.loads(base64.b64decode(start_b64))
                end: datetime = pickle.loads(base64.b64decode(end_b64))
                is_inside = is_inside or (start <= time <= end)

        return is_inside
