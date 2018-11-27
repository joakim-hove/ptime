from django.test import TransactionTestCase, Client


from ptime.server.tests.context import Context as ServerContext
from ptime.client import PTimeClient, run

class ClientTest(TransactionTestCase):

    def setUp(self):
        self.server_context = ServerContext()


    def Xtest_command(self):
        with self.assertRaises(ValueError):
            client = PTimeClient([])


        with self.assertRaises(KeyError):
            client = PTimeClient(["UNKNONW_COMMAND"])

        with self.assertRaises(ValueError):
            client = PTimeClient(["start"])


        client = PTimeClient(["stop"])
        client = PTimeClient(["start", "sleipner"])
        status, data = client.run()
        self.assertEqual(status, 201)
        self.assertIn("started_task", data)
        self.assertNotIn("active_task", data)
        self.assertNotIn("completed_task", data)


        client = PTimeClient(["stop"])
        status, data= client.run()
        self.assertEqual(status, 201)
        self.assertIn("completed_task", data)
        self.assertNotIn("started_task", data)
        self.assertNotIn("active_task", data)
