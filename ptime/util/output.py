from .time import *


def print_task(prefix, task):
    project = task["project"]
    if "activity" in task:
        project += "/{}".fomat(task["activity"])

    start_time = parse_date(task["start_time"])
    start_str = format_time(start_time)

    end_time = None
    if "end_time" in task:
        end_time = parse_date(task["end_time"])
    else:
        dt = datetime.datetime.utcnow() - start_time
        if dt.total_seconds() > 1:
            end_time = datetime.datetime.utcnow()

    if end_time:
        end_str = " -- {:8s}".format( format_time(end_time) )

        hours,minutes,_ = split_time(end_time - start_time)

        dur_str = "[{} hours {} minutes]".format(hours, minutes)
    else:
        end_str = " --       "
        dur_str = ""



    s = "{:16}: {:16}  {:5s} {:6s}   {}".format(prefix, project, start_str, end_str, dur_str)
    print(s)
