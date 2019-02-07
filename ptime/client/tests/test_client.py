import json

from django.test import TransactionTestCase, Client
from django.urls import reverse

from ptime.server.tests.context import Context as ServerContext
from ptime.server.models import *
from ptime.client import PTimeClient, run
from ptime.client.ptime_client import BaseClient, parse_args
from ptime.util import *


class ClientTest(TransactionTestCase):

    def setUp(self):
        self.server_context = ServerContext()
        # Could check that the testserver is running in a different process,
        # and in that case the run_client attribute could be set to True.
        self.run_client = False


    def test_command(self):
        with self.assertRaises(KeyError):
            client = PTimeClient("unknown_command", None)

        with self.assertRaises(ValueError):
            client = PTimeClient("start", parse_args("start", []))


        client = PTimeClient("stop", parse_args("stop", []))
        data = client.data()
        self.assertIn("user", data)

        client = PTimeClient("start", parse_args("start", ["sleipner"]))
        data = client.data()
        self.assertIn("user", data)

        client = PTimeClient("start", parse_args("start", ["sleipner", "python3"]))
        data = client.data()
        self.assertIn("user", data)
        self.assertIn("activity", data)

        if self.run_client:
            status, data = client.run()

            self.assertEqual(status, 201)
            self.assertIn("started_task", data)
            self.assertNotIn("active_task", data)
            self.assertNotIn("completed_task", data)


        client = PTimeClient("stop", parse_args("stop", []))
        if self.run_client:
            status, data= client.run()

            self.assertEqual(status, 201)
            self.assertIn("completed_task", data)
            self.assertNotIn("started_task", data)
            self.assertNotIn("active_task", data)


    def test_time(self):
        hour = 11
        minute = 12
        user = self.server_context.user1
        argv = [str(self.server_context.project1),
                "--start={}:{}".format(hour, minute),
                "--user={}".format(user.username)]

        ptime_client = PTimeClient("stop", parse_args("start", argv))
        dt = parse_date(ptime_client.data()["start"])
        print("dt: {}".format(dt))
        data = ptime_client.data()

        # Could ideally let the PtimeClient() interact transparently through the
        # django test client.
        start_url = reverse("api.task.start", args = [self.server_context.project1.short_name])
        django_client = Client()
        response = django_client.post(start_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        wip = WIP.objects.get(who = user)
        wip_data = wip.task_dict()

        print(str(wip_data["start_time"]))
        wip_start = parse_date(str(wip_data["start_time"]))
        self.assertEqual(wip_start.hour, hour)
        self.assertEqual(wip_start.minute, minute)
