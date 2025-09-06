from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # Tasks
    path("tasks/<int:project_id>/", views.task_inside_view, name="task_inside_view"),
    path("mytaskview/", views.taskview, name="taskview"),

    # Projects
    path("projectsnew/", views.new_project, name="new_project"),   # New Project page
    path("projectssave/", views.save_project, name="save_project"),
    path("create_project/", views.save_project, name="create_project"),

    # 👇 New: Task Create + Save (project ke andar)
    path("tasknew/<int:project_id>/", views.new_task, name="new_task"),  # project id chahiye
    path("tasksave/<int:project_id>/", views.save_task, name="save_task"), # project id pass hoga
]
