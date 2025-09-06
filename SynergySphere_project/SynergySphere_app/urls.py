from django.urls import path
from . import views

urlpatterns = [
    # ---------------- HOME ----------------
    path('', views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # ---------------- TASKS ----------------
    path("tasks/<int:project_id>/", views.task_inside_view, name="task_inside_view"),   # Project ke andar tasks
    path("mytasks/", views.taskview, name="taskview"),                                  # All my tasks

    path("tasks/new/<int:project_id>/", views.new_task, name="new_task"),               # New Task (needs project_id)
    path("tasks/save/<int:project_id>/", views.save_task, name="save_task"),            # Save Task (needs project_id)

    # ---------------- PROJECTS ----------------
    path("projects/new/", views.new_project, name="new_project"),                       # Project create form
    path("projects/save/", views.save_project, name="save_project"),                    # Save Project
    # extra create_project path hata sakte ho (duplicate hai), ya redirect kar do
    # path("create_project/", views.save_project, name="create_project"),               

]
