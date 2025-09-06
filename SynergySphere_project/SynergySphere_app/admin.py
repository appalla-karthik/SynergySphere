from django.contrib import admin
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "manager", "priority", "status", "deadline", "created_at")
    search_fields = ("name", "manager", "tags")

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project", "assignee", "status", "deadline", "created_at")
    search_fields = ("name", "assignee", "tags")
    list_filter = ("status", "deadline")
