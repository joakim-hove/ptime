import datetime
import django.utils.dateparse
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
TIME_ZONE = "Europe/Oslo"

def parse_date(date_str):
    dt = django.utils.dateparse.parse_datetime(date_str)
    return dt

def format_time(dt):
    diff = datetime.datetime.now() - datetime.datetime.utcnow()
    dt += diff
    return dt.strftime("%H:%M")

def format_date(dt):
    return dt.strftime("%Y-%m-%d")


def utc(func):
    def wrapper(input_string):
        naive_dt = func(input_string)
        aware_dt = naive_dt.replace(tzinfo=datetime.timezone.utc)
        return aware_dt
    return wrapper


@utc
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
