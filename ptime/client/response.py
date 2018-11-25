import datetime
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

def _parse_date(date_str):
    return datetime.datetime.strptime(date_str, DATETIME_FORMAT)


class Duration(object):

    def __init__(self, dt):
        seconds = dt.total_seconds()
        self.hours   = int(seconds // 3600)
        self.minutes = int((seconds - self.hours * 3600) // 60)
        self.seconds = int(seconds - self.hours * 3600 - self.minutes * 60)


    def __str__(self):
        return "{:2d}:{:02d}".format(self.hours, self.minutes)



class Task(object):

    def __init__(self, data):
        if "activity" in data:
            self.project = "{0}/{1}".format(data["project"], data["activity"])
        else:
            self.project = data["project"]
        self.start_time = _parse_date( data["start_time"] )
        if "end_time" in data:
            self.end_time = _parse_date(data["end_time"])
            self.duration = Duration( self.end_time - self.start_time )
        else:
            self.end_time = None
            self.duration = None



class Response(object):

    def __init__(self, status_code, data):
        self.status_code = status_code
        self.completed_task = None
        self.started_task = None

        if "completed_task" in data:
            self.completed_task = Task(data["completed_task"])

        if "started_task" in data:
            self.started_task = Task(data["started_task"])


