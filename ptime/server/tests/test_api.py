import json

from django.urls import reverse
from django.utils import timezone
from django.test import TransactionTestCase, Client
from django.db.utils import IntegrityError

from ptime.server.models import *
from .context import Context


class WorkAPITest(TransactionTestCase):

    def setUp(self):
        self.context = Context()


    def test_start(self):
        url1 = reverse("api.task.start", args = [self.context.project1.short_name])
        url2 = reverse("api.task.start", args = [self.context.project2.short_name])
        client = Client()
        response = client.get(url1)
        self.assertEqual(response.status_code, 405)

        valid_params =  {"user" : self.context.user1.username}

        response = client.post(url1, json.dumps(valid_params), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content.decode('utf-8'))
        started_task = data["started_task"]
        self.assertEqual(started_task["project"], self.context.project1.short_name)
        self.assertFalse("completed_task" in data)

        response = client.post(url2, json.dumps(valid_params), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data["started_task"]["project"], self.context.project2.short_name)
        self.assertEqual(data["completed_task"]["project"], self.context.project1.short_name)


    def test_stop(self):
        stop_url = reverse("api.task.stop")
        start_url = reverse("api.task.start", args=[self.context.project1.short_name])
        client = Client()
        response = client.get(stop_url)
        self.assertEqual(response.status_code, 405)

        response = client.post(stop_url , json.dumps({"user" : self.context.user1.username}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertFalse("completed_task" in data)

        response = client.post(start_url , json.dumps({"user" : self.context.user1.username}), content_type="application/json")
        response = client.post(stop_url , json.dumps({"user" : self.context.user1.username}), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data["completed_task"]["project"], self.context.project1.short_name)

        response = client.post(stop_url , json.dumps({"user" : self.context.user1.username}), content_type="application/json")
        self.assertEqual(response.status_code, 200)