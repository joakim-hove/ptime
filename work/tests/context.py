from django.contrib.auth.models import User
from work.models import *


class Context(object):
    def __init__(self):
        self.user1 = User.objects.create(username = "name1",
                                         email = "name@email.com",
                                         password = "Secret")

        self.user2 = User.objects.create(username = "name2",
                                         email = "name@email.com",
                                         password = "Secret")

        self.project = Project.objects.create(short_name = "opm",
                                              name = "OPM Project"
                                              description = "Long description")

        self.activity = Activity.objects.create(short_name = "operater",
                                                name = "Implement support for OPERATER keyword"
                                                project = self.project)
        self.object_list = [self.user1,
                            self.user2,
                            self.project,
                            self.activity]

    def save(self):
        for obj in self.object_list:
            obj.save()
