from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("tasks/<int:project_id>/", views.task_inside_view, name="task_inside_view"),   
    path("mytasks/", views.taskview, name="taskview"),                                  

    path("tasks/new/<int:project_id>/", views.new_task, name="new_task"),              
    path("tasks/save/<int:project_id>/", views.save_task, name="save_task"),            

   
    path("projectsnew/", views.new_project, name="new_project"),                       
    path("projects/save/", views.save_project, name="save_project"),                   
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),    
    path("project/<int:project_id>/add-people/", views.add_people, name="add_people"),
    path("search-users/", views.search_users, name="search_users"),

    path("profile/", views.profile_view, name="profile"),
]
