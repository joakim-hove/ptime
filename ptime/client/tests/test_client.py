from django.test import TransactionTestCase, Client


from ptime.server.tests.context import Context as ServerContext
from ptime.client import PTimeClient, run
from ptime.client.ptime_client import BaseClient, parse_args


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



