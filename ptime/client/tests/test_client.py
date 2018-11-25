from django.test import TransactionTestCase, Client


from ptime.server.tests.context import Context as ServerContext
from ptime.client import PTimeClient

class ClientTest(TransactionTestCase):

    def setUp(self):
        self.server_context = ServerContext()


    def test_command(self):
        with self.assertRaises(ValueError):
            client = PTimeClient([])


        with self.assertRaises(KeyError):
            client = PTimeClient(["UNKNONW_COMMAND"])

        with self.assertRaises(ValueError):
            client = PTimeClient(["start"])

        client = PTimeClient(["start", "sleipner"])
        response = client.run()
        print(response, response.text)
