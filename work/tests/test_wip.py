from django.utils import timezone
from django.test import TransactionTestCase, Client
from django.db.utils import IntegrityError

from work.models import *
from .context import Context


class WIPTest(TransactionTestCase):

    def setUp(self):
        self.context = Context()

    def test_create(self):
        wip1 = WIP.objects.create(who = self.context.user1,
                                  project = self.context.project)

        self.assertIsNone(wip1.activity)
        self.context.project.default_activity = self.context.activity
        self.context.save()

        wip2 = WIP.objects.create(who = self.context.user2,
                                  project = self.context.project)
        self.assertEqual( wip2.activity, self.context.activity )

        with self.assertRaises(IntegrityError):
            wip3 = WIP.objects.create(who = self.context.user2,
                                      project = self.context.project)

        len0 = len(TaskRecord.objects.all())
        task_record = WIP.complete(self.context.user1)
        print(task_record)
        self.assertIsNotNone( task_record )
        with self.assertRaises(WIP.DoesNotExist):
            wip1.refresh_from_db()
        self.assertIsNone( WIP.complete(self.context.user1))
        len1 = len(TaskRecord.objects.all())

        self.assertEqual(len1 - len0, 1)

        wip1 = WIP.objects.create(who = self.context.user1,
                                  project = self.context.project)


        WIP.cancel(self.context.user2)
        
