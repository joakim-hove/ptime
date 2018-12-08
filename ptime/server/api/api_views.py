from django.views.decorators.csrf import csrf_exempt
import json

from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from ptime.server.models import *


@csrf_exempt
def start_task(request, project_id):
    if not request.method == "POST":
        return HttpResponse("Only method POST allowed", status = 405)

    params = json.loads(request.body.decode('utf-8'))
    try:
        user = User.objects.get( username=params["user"])
    except User.DoesNotExist:
        return HttpResponse("Invalid user:{}".format(params["user"]), status=403)


    try:
        start_project = Project.objects.get( short_name = project_id )
    except Project.DoesNotExist:
        return HttpResponse("Project: {} does not exist".format(project_id), status=404)


    if "activity" in params:
        try:
            activity = Activity.objects.get(project=start_project, short_name=params["activity"])
        except Activity.DoesNotExist:
            return HttpResponse("Activity: {} does not exist".format(params["actvity"]), status=404)
    else:
        activity = start_project.default_activity


    if "start_time" in params:
        start_time = timezone.now()
    else:
        start_time = timezone.now()

    completed_task = WIP.complete(user)
    wip = WIP.start(user, start_project, start_time, activity = activity)

    started_task = {"project" : wip.project.short_name,
                    "start_time" : wip.start_time}
    if wip.activity:
        started_task["activity"] = wip.activity.short_name

    response = {"started_task" : started_task}

    if completed_task:
        response["completed_task"] = completed_task.to_dict()

    return JsonResponse(response, status=201)


@csrf_exempt
def stop_task(request):
    if not request.method == "POST":
        return HttpResponse("Only method POST allowed", status = 405)

    params = json.loads(request.body.decode('utf-8'))
    try:
        user = User.objects.get( username=params["user"])
    except User.DoesNotExist:
        return HttpResponse("Invalid user:{}".format(params["user"]), status=403)

    if "end_time" in params:
        pass
    else:
        end_time = None

    completed_task = WIP.complete(user, end_time)
    if completed_task:
        response = {"completed_task" : completed_task.to_dict() }
        return JsonResponse(response, status=201)
    else:
        response = {}
        return JsonResponse(response, status=200)


def status(request):
    user = request.GET.get("user")
    if not user:
        return HttpResponse("Missing user", status=403)

    try:
        user = User.objects.get( username = user )
    except User.DoesNotExist:
        return HttpResponse("Invalid user:{}".format(user), status=403)

    response = {}
    try:
        wip = WIP.objects.get( who=user )
        response["active_task"] = wip.task_dict()
    except WIP.DoesNotExist:
        pass

    return JsonResponse(response, status=200)



def get(request):
    user = request.GET.get("user")
    if not user:
        return HttpResponse("Missing user", status=403)

    try:
        user = User.objects.get( username = user )
    except User.DoesNotExist:
        return HttpResponse("Invalid user:{}".format(user), status=403)

    record_query = TaskRecord.objects.all()
    response = { "task_list" : [ record.to_dict() for record in record_query ]}

    return JsonResponse(response, status=200)
