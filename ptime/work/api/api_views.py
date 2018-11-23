import json

from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from ptime.work.models import *


def start_task(request, project_id):
    if not request.method == "POST":
        return HttpResponse("Only method POST allowed", status = 405)

    params = json.loads(request.body.decode('utf-8'))
    start_project = get_object_or_404(Project, short_name = project_id)
    user = get_object_or_404(User, username=params["user"])

    if "activity" in params:
        activity = get_object_or_404(Activity, short_name=params["activity"])
    else:
        activity = start_project.default_activity

    if "start_time" in params:
        start_time = timezone.now()
    else:
        start_time = timezone.now()

    completed_task = WIP.complete(user)
    wip = WIP.start(user, start_project, start_time, activity = activity)

    task = None
    if completed_task:
        task = completed_task.to_dict()
    response = {"completed_task" : task,
                "started_task" : {"project" : wip.project.short_name,
                                  "start_time" : wip.start_time}}

    return JsonResponse(response, status=201)



def stop_task(request):
    if not request.method == "POST":
        return HttpResponse("Only method POST allowed", status = 405)

    params = json.loads(request.body.decode('utf-8'))
    user = get_object_or_404(User, username=params["user"])
    if "end_time" in params:
        pass
    else:
        end_time = None

    completed_task = WIP.complete(user, end_time)
    if completed_task:
        response = {"completed_task" : completed_task.to_dict() }
        return JsonResponse(response, status=201)
    else:
        response = {"completed_task" : None}
        return JsonResponse(response, status=200)

