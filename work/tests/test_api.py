import json

from django.urls import reverse
from django.utils import timezone
from django.test import TransactionTestCase, Client
from django.db.utils import IntegrityError

from work.models import *
from .context import Context


class WorkAPITest(TransactionTestCase):

    def setUp(self):
        self.context = Context()


    def test_start(self):
        url = reverse("api.task.start", args = [self.context.project.short_name])
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 405)

        valid_params =  {"user" : self.context.user1.username,
                         "project" : self.context.project.short_name}

        response = client.post(url, json.dumps(valid_params), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content.decode('utf-8'))

