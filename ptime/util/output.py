import django.utils.timezone
from .time import *


def fmt_task(prefix, task):
    project = task["project"]
    if "activity" in task:
        project += "/{}".format(task["activity"])

    start_time = parse_date(task["start_time"])
    start_str = format_time(start_time)

    end_time = None
    if "end_time" in task:
        end_time = parse_date(task["end_time"])
    else:
        now = django.utils.timezone.now()
        dt = now - start_time
        if dt.total_seconds() > 1:
            end_time = now

    if end_time:
        end_str = " -- {:8s}".format( format_time(end_time) )

        hours,minutes,_ = split_time(end_time - start_time)

        dur_str = "[{} hours {} minutes]".format(hours, minutes)
    else:
        end_str = " --       "
        dur_str = ""


    s = "{:16}: {:16}  {:5s} {:6s}   {}".format(prefix, project, start_str, end_str, dur_str)
    return s




def print_summary(start_time, end_time, sum_dict):
    width = 70
    short_width = 50
    print("\n")
    print("=" * width)
    print("Start: {}".format( format_date( parse_date(start_time))))
    print("End:   {}".format( format_date( parse_date(end_time))))
    print("-" * width)

    project_count = 0
    for project in sum_dict.keys():
        total_time = sum_dict[project]["__total__"]
        hours, minutes, _ = split_time( total_time )
        time_string = "{:2d}:{:02d}".format(hours, minutes)
        pad = " " * (width - len(project) - len(time_string))
        print("{}{}{}".format(project, pad, time_string))

        for key in sum_dict[project]:
            if key != "__total__":
                total_time = sum_dict[project][key]
                hours, minutes, _ = split_time( total_time )
                time_string = "{:2d}:{:02d}".format(hours, minutes)
                pad = " " * (short_width - len(project) - len(time_string) - len(key) - 1)
                print("{}/{}{}{}".format(project, key, pad, time_string))
        project_count += 1
        if project_count < len(sum_dict.keys()):
            print()

    print("=" * width)
    print("\n")
