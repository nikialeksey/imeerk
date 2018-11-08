import shutil
import tempfile
from datetime import datetime
from os import path
from unittest import TestCase

from imeerk.calendars.icalendar import FileTimeIntervals


class FileTimeIntervalsTest(TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add(self):
        file = path.join(self.test_dir, 'test.txt')
        intervals = FileTimeIntervals(file)
        intervals.add(datetime(2018, 9, 15, 0, 0), datetime(2018, 9, 16, 0, 0), 'asd')
        self.assertTrue(intervals.is_inside(datetime(2018, 9, 15, 1, 1)))
