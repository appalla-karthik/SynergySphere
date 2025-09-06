from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # ---------------- TASKS ----------------
    path("tasks/<int:project_id>/", views.task_inside_view, name="task_inside_view"),  # Project ke andar tasks
    path("mytaskview/", views.taskview, name="taskview"),                             # My tasks page

    path("tasks/new/<int:project_id>/", views.new_task, name="new_task"),             # New Task (needs project_id)
    path("tasks/save/<int:project_id>/", views.save_task, name="save_task"),          # Save Task (needs project_id)

    # ---------------- PROJECTS ----------------
    path("projectsnew/", views.new_project, name="new_project"),
    path("projectssave/", views.save_project, name="save_project"),
    path("create_project/", views.save_project, name="create_project"),
]
