import json
import pytz
from django.test import TestCase

from ptime.server.tests import Context as ServerContext
from ptime.server.models import *
from ptime.util import *

TIME_ZONE = "Europe/Oslo"

class TimeTest(TestCase):

    def setUp(self):
        pass

    def test_input_date(self):
        input = datetime.datetime.utcnow()
        dt = parse_input_date(input.strftime("%d/%m/%Y"))
        self.assertEqual(dt.day, input.day)
        self.assertEqual(dt.month, input.month)
        self.assertEqual(dt.year, input.year)

        dt = parse_input_date(input.strftime("%d/%m/%y"))
        self.assertEqual(dt.day, input.day)
        self.assertEqual(dt.month, input.month)
        self.assertEqual(dt.year, input.year)

        dt = parse_input_date(input.strftime("%d/%m"))
        self.assertEqual(dt.day, input.day)
        self.assertEqual(dt.month, input.month)
        self.assertEqual(dt.year, input.year)

        dt = parse_input_date(input.strftime("-1"))
        input += datetime.timedelta(days = -1)
        self.assertEqual(dt.day, input.day)
        self.assertEqual(dt.month, input.month)
        self.assertEqual(dt.year, input.year)



    def test_input_time(self):
        input = pytz.timezone(TIME_ZONE).localize( datetime.datetime.now() )
        dt = parse_input_time(input.strftime("%H:%M"))
        diff = input - dt
        self.assertTrue(abs(diff.total_seconds()) < 61)

        dt = parse_input_time("+1:30")
        diff = input - dt + datetime.timedelta(seconds=5400)
        self.assertTrue(abs(diff.total_seconds()) < 61)

        dt = parse_input_time("-1")
        diff = input - dt + datetime.timedelta(seconds=-3600)
        self.assertTrue(abs(diff.total_seconds()) < 61)

        None_date = parse_date(None)
        self.assertIsNone(None_date)
        date_str = format_date(None)
        self.assertEqual(date_str, "[  Now   >")


    def test_conversions(self):
        naive_dt = datetime.datetime.now()
        self.assertFalse(is_aware(naive_dt))

        with self.assertRaises(ValueError):
            parse_date("2020-10-10")

        aware_dt = pytz.timezone(TIME_ZONE).localize(naive_dt)
        self.assertTrue(is_aware(aware_dt))

        oslo = pytz.timezone("Europe/Oslo")
        utc = pytz.timezone("UTC")
        oslo_dt = oslo.localize(naive_dt)

        utc_dt = change_tzone(oslo_dt, utc)
        print(utc_dt)
        print(oslo_dt)
        self.assertTrue( utc_dt.hour < oslo_dt.hour )


