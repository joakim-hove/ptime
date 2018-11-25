from django.utils import timezone
from django.test import TransactionTestCase, Client
from django.db.utils import IntegrityError

from ptime.server.models import *
from .context import Context


class WIPTest(TransactionTestCase):

    def setUp(self):
        self.context = Context()

    def test_create(self):
        wip1 = WIP.objects.create(who = self.context.user1,
                                  project = self.context.project1)

        self.assertIsNone(wip1.activity)
        self.context.project1.default_activity = self.context.activity1
        self.context.save()

        wip2 = WIP.start(who = self.context.user2,
                         project = self.context.project1)
        self.assertEqual( wip2.activity, self.context.activity1 )
        self.assertEqual( self.context.project1.activity_name(), "{}/{}".format(self.context.project1.short_name,
                                                                                self.context.activity1.short_name))

        with self.assertRaises(IntegrityError):
            wip3 = WIP.objects.create(who = self.context.user2,
                                      project = self.context.project1)

        len0 = len(TaskRecord.objects.all())
        task_record = WIP.complete(self.context.user1)
        self.assertIsNotNone( task_record )
        with self.assertRaises(WIP.DoesNotExist):
            wip1.refresh_from_db()
        self.assertIsNone( WIP.complete(self.context.user1))
        len1 = len(TaskRecord.objects.all())

        self.assertEqual(len1 - len0, 1)

        wip1 = WIP.objects.create(who = self.context.user1,
                                  project = self.context.project1)


        WIP.cancel(self.context.user2)

        wip = WIP.start(self.context.user2, self.context.project1)
