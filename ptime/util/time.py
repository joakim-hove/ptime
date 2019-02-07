import re
import datetime
import time
import django.utils.dateparse
import pytz

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
TIME_ZONE = "Europe/Oslo"

def parse_date(date_str):
    if date_str is None:
        return None

    dt = django.utils.dateparse.parse_datetime(date_str)
    return dt

def format_time(dt):
    return dt.strftime("%H:%M")

def format_date(dt):
    if dt is None:
        return "[  Now   >"

    return dt.strftime("%Y-%m-%d")


def localtime(func):
    def wrapper(input_string):
        naive_dt = func(input_string)
        aware_dt = pytz.timezone(TIME_ZONE).localize(naive_dt)
        return aware_dt
    return wrapper


def add_date(func):
    def wrapper(input_string):
        t = func(input_string)
        today = datetime.date.today()
        return datetime.datetime(today.year, today.month, today.day, t.tm_hour, t.tm_min, t.tm_sec)
    return wrapper


@localtime
def parse_input_date(input_string):
    date_format = "%d/%m/%y"
    try:
        return datetime.datetime.strptime(input_string, date_format)
    except ValueError:
        pass


    date_format = "%d/%m/%Y"
    try:
        return datetime.datetime.strptime(input_string, date_format)
    except ValueError:
        pass


    now = datetime.datetime.utcnow()
    day_month_format = "%d/%m"
    try:
        dt = datetime.datetime.strptime(input_string, day_month_format)
        dt = dt.replace( year = now.year )
        return dt
    except ValueError:
        pass


    try:
        days = int(input_string)
        return now + datetime.timedelta( days = days)
    except ValueError:
        pass


@localtime
def parse_input_time(input_string):
    try:
       t = time.strptime(input_string, "%H:%M")
       today = datetime.date.today()
       return datetime.datetime(today.year, today.month, today.day, t.tm_hour, t.tm_min, t.tm_sec)
    except ValueError:
        pass

    now = datetime.datetime.utcnow()
    time_re = re.compile("^(?P<sign>[+-])(?P<hours>\d+):(?P<minutes>\d+)$")
    match_obj = time_re.match(input_string)
    if match_obj:
        hours = int( match_obj.group("hours"))
        minutes = int(match_obj.group("minutes"))
        sign = match_obj.group("sign")
        seconds = hours * 3600 + minutes * 60
        if sign == "-":
            seconds *= -1

        return now + datetime.timedelta(seconds = seconds)

    time_re = re.compile("^(?P<sign>[+-])(?P<hours>\d+)$")
    match_obj = time_re.match(input_string)
    if match_obj:
        hours = int( match_obj.group("hours"))
        sign = match_obj.group("sign")
        seconds = hours * 3600
        if sign == "-":
            seconds *= -1

        return now + datetime.timedelta(seconds = seconds)





class Duration(object):

    def __init__(self, dt):
        seconds = dt.total_seconds()
        self.hours   = int(seconds // 3600)
        self.minutes = int((seconds - self.hours * 3600) // 60)
        self.seconds = int(seconds - self.hours * 3600 - self.minutes * 60)


    def __str__(self):
        return "{:2d}:{:02d}".format(self.hours, self.minutes)



    def split(self):
        return self.hours, self.minutes, self.seconds


def split_time(dt):
    if not isinstance(dt, datetime.timedelta):
        dt = datetime.timedelta( seconds = dt )

    dur = Duration(dt)
    return dur.split()
