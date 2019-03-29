from django.contrib.auth.models import User
from ptime.server.models import *


class Context(object):
    def __init__(self):
        self.user1 = User.objects.create(username = "name1",
                                         email = "name@email.com",
                                         password = "Secret")

        self.user2 = User.objects.create(username = "name2",
                                         email = "name@email.com",
                                         password = "Secret")

        self.project1 = Project.objects.create(short_name = "opm",
                                              name = "OPM Project")

        self.project2 = Project.objects.create(short_name = "ERT",
                                              name = "OPM Project")

        self.activity1 = Activity.objects.create(short_name = "operater",
                                                project = self.project1)

        self.activity2 = Activity.objects.create(short_name = "operater",
                                                project = self.project2)

        self.record1 = TaskRecord.objects.create(start_time=timezone.now() - datetime.timedelta(hours=6),
                                                 end_time=timezone.now(),
                                                 who=self.user1,
                                                 project=self.project1)

        self.record2 = TaskRecord.objects.create(start_time=timezone.now() - datetime.timedelta(hours=6),
                                                 end_time=timezone.now(),
                                                 who=self.user2,
                                                 project=self.project2)


        self.object_list = [self.user1,
                            self.user2,
                            self.project1,
                            self.project2,
                            self.activity1,
                            self.activity2,
                            self.record1,
                            self.record2]

    def save(self):
        for obj in self.object_list:
            obj.save()
