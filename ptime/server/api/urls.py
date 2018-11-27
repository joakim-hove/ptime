from django.urls import include, path

from .api_views import start_task, stop_task, status

urlpatterns = [
    path("status/", status, name = "api.status"),
    path("task/start/<str:project_id>/", start_task, name = "api.task.start"),
    path("task/stop/", stop_task, name = "api.task.stop")
]
