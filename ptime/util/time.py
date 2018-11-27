import datetime
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

def parse_date(date_str):
    tz_time = datetime.datetime.strptime(date_str, DATETIME_FORMAT)
    return tz_time

def format_time(dt):
    diff = datetime.datetime.now() - datetime.datetime.utcnow()
    dt += diff
    return dt.strftime("%H:%M")


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
    dur = Duration(dt)
    return dur.split()