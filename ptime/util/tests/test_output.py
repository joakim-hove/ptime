import json
from django.test import TestCase

from ptime.server.tests import Context as ServerContext
from ptime.server.models import *
from ptime.util import *
from ptime.util.time import DATETIME_FORMAT

class OutputTest(TestCase):

    def setUp(self):
        self.server_context = ServerContext()

    def test_output(self):
        wip = WIP.start(self.server_context.user1, self.server_context.project1)
        d = wip.task_dict()
        d["start_time"] = d["start_time"].strftime(DATETIME_FORMAT)
        s = fmt_task("prefix", d)
