class Task(object):

    def __init__(self, data):
        self.project = data["project"]
        self.seconds = data["seconds"]
        self.activity = data.get("activity")



def task_summary(task_list):
    sum_dict = {}
    for task_data in task_list:
        task = Task(task_data)

        if not task.project in sum_dict:
            sum_dict[task.project] = {"__total__": 0}

        sum_dict[task.project]["__total__"] += task.seconds
        if task.activity:
            if not task.activity in sum_dict[task.project]:
                sum_dict[task.project][task.activity] = 0

            sum_dict[task.project][task.activity] += task.seconds

    return sum_dict
