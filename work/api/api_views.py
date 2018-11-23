import json

from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from work.models import *


def start_task(request, project_id):
    if not request.method == "POST":
        return HttpResponse("Only method POST allowed", status = 405)

    params = json.loads(request.body.decode('utf-8'))
    project = get_object_or_404(Project, short_name = project_id)
    user = get_object_or_404(User, username=params["user"])

    if "activity" in params:
        activity = get_object_or_404(Activity, short_name=params["activity"])
    else:
        activity = None

    if "start_time" in params:
        start_time = timezone.now()
    else:
        start_time = timezone.now()

    completed_task = WIP.complete(user)
    wip = WIP.start(user, project, start_time, activity = activity)

    task = None
    if completed_task:
        task = model_to_dict(completed_task)
        task["project"] = completed_task.project.short_name
        if task["activity"]:
            task["activity"] = completed_task.activity.short_name

    response = {"completed_task" : task,
                "started_task" : {"project" : wip.project.short_name,
                                  "start_time" : wip.start_time}}

    return JsonResponse(response, status=201)
