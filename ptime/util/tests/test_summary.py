import json
from django.test import TestCase
from django.utils.timezone import now
from ptime.server.tests import Context as ServerContext
from ptime.server.models import *
from ptime.util import *
from ptime.util.time import DATETIME_FORMAT

class OutputTest(TestCase):

    def setUp(self):
        self.server_context = ServerContext()
        start_time = now() - datetime.timedelta(seconds = 3600)
        self.task_list = []
        for task_nr in range(10):
            rec = TaskRecord.objects.create(start_time = start_time,
                                            end_time = now(),
                                            who = self.server_context.user1,
                                            project = self.server_context.project1)
            self.task_list.append(rec)


        for task_nr in range(10):
            rec = TaskRecord.objects.create(start_time = start_time,
                                            end_time = now(),
                                            who = self.server_context.user1,
                                            activity = self.server_context.activity1,
                                            project = self.server_context.project1)
            self.task_list.append(rec)


    def test_summary(self):
        task_list = [ task.to_dict() for task in self.task_list ]
        sum_dict = task_summary(task_list)

        self.assertIn(self.server_context.project1.short_name, sum_dict)
