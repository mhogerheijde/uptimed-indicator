import unittest

from uptime_indicator.cli import *
from datetime import timedelta


class TestIndicator(unittest.TestCase):

    def test_fromatAsHoursMinutesFormatsPositiveDelta(self):
        # SETUP
        delta1 = timedelta(hours=1, minutes=42, seconds=1)
        expect1 = "01:42:01"

        delta2 = timedelta(days=1, hours=1, minutes=42, seconds=1)
        expect2 = "25:42:01"

        # CALL
        result1 = fromatAsHoursMinutes(delta1, includeSeconds=True)
        result2 = fromatAsHoursMinutes(delta2, includeSeconds=True)

        # VERIFY
        self.assertEqual(result1, expect1)
        self.assertEqual(result2, expect2)

    def test_fromatAsHoursMinutesFormatsZeroDelta(self):
        # SETUP
        delta = timedelta(hours=0, minutes=0, seconds=0)
        expect = "00:00:00"

        # CALL
        result = fromatAsHoursMinutes(delta, includeSeconds=True)

        # VERIFY
        self.assertEqual(result, expect)

    def test_fromatAsHoursMinutesFormatsNegative(self):
        # SETUP
        delta1 = timedelta(days=0, hours=0, minutes=-30, seconds=3)
        expect1 = "-00:29:57"

        delta2 = timedelta(days=-1, hours=-20, minutes=-30, seconds=-3)
        expect2 = "-44:30:03"

        # CALL
        result1 = fromatAsHoursMinutes(delta1, includeSeconds=True)
        result2 = fromatAsHoursMinutes(delta2, includeSeconds=True)

        # VERIFY
        self.assertEqual(result1, expect1)
        self.assertEqual(result2, expect2)

    def test_formatAsDecimalFormatsPositiveDelta(self):
        # SETUP
        delta1 = timedelta(hours=1, minutes=33, seconds=1)
        expect1 = "1.55"

        delta2 = timedelta(days=1, hours=1, minutes=42, seconds=1)
        expect2 = "25.70"

        # CALL
        result1 = fromatAsDecimalHours(delta1)
        result2 = fromatAsDecimalHours(delta2)

        # VERIFY
        self.assertEqual(result1, expect1)
        self.assertEqual(result2, expect2)

    def test_formatAsDecimalFormatsNegativeDelta(self):
        # SETUP
        delta1 = timedelta(hours=-1, minutes=42, seconds=1)
        expect1 = "-0.30"

        delta2 = timedelta(days=-11, hours=1, minutes=42, seconds=1)
        expect2 = "-262.30"

        # CALL
        result1 = fromatAsDecimalHours(delta1)
        result2 = fromatAsDecimalHours(delta2)

        # VERIFY
        self.assertEqual(result1, expect1)
        self.assertEqual(result2, expect2)
