from django.urls import include, path

from .api_views import start_task

urlpatterns = [
    path("task/start/<str:project_id>/", start_task, name = "api.task.start")
]
