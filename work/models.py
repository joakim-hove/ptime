import datetime

from django.core import serializers
from django.db.models import *
from django.contrib.auth.models import User
from django.utils import timezone


class Project(Model):
    short_name = CharField(max_length=16, unique=True)
    name = CharField(max_length=80)
    start_time = DateField(default = datetime.date.today)
    description = CharField(max_length=512, blank=True, null=True)
    default_activity = ForeignKey("Activity", blank=True, null=True, on_delete=SET_NULL, related_name="default_activity")


    def __str__(self):
        return self.name


class Activity(Model):
    short_name = CharField(max_length=16)
    start_time = DateField(default = datetime.date.today)
    description = CharField(max_length=512, blank=True, null=True)
    project = ForeignKey(Project, on_delete=CASCADE)

    def __str__(self):
        return self.name



class TaskRecord(Model):
    start_time = DateTimeField()
    end_time = DateTimeField()
    who = ForeignKey(User, on_delete=PROTECT)
    project = ForeignKey(Project, on_delete=PROTECT)
    activity = ForeignKey(Activity, blank=True, null=True, on_delete=PROTECT)
    comment = CharField(max_length=512, blank=True, null=True)


class WIP(Model):
    project = ForeignKey(Project, on_delete=CASCADE)
    activity = ForeignKey(Activity, on_delete=CASCADE, blank=True, null=True)
    who = OneToOneField(User, on_delete=CASCADE)
    start_time = DateTimeField(default = timezone.now)
    comment = CharField(max_length=512, blank=True, null=True)



    @classmethod
    def complete(cls, user, end_time = None):
        try:
            wip = cls.objects.get(who = user)
        except cls.DoesNotExist:
            return None

        if end_time is None:
            end_time = timezone.now()

        task_record = TaskRecord.objects.create(start_time = wip.start_time,
                                                end_time = end_time,
                                                who = wip.who,
                                                project = wip.project,
                                                activity = wip.activity,
                                                comment = wip.comment)
        wip.delete()
        return task_record


    @classmethod
    def cancel(cls, user):
        try:
            wip = cls.objects.get(who = user)
            wip.delete()
        except cls.DoesNotExist:
            pass


    @classmethod
    def start(cls, who, project, start_time=None, activity=None):
        if start_time is None:
            start_time = timezone.now()

        if activity is None:
            activity = project.default_activity

        wip = cls.objects.create(project = project,
                                 who = who,
                                 activity = activity,
                                 start_time = start_time)
        return wip
