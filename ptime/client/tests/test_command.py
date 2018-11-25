from django.test import TransactionTestCase, Client


from ptime.server.tests.context import Context as ServerContext
from ptime.client import PTimeClient

class ClientTest(TransactionTestCase):

    def setUp(self):
        self.server_context = ServerContext()


    def test_command(self):
        pass
