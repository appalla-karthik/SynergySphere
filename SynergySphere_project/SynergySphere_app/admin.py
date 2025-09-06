from django.contrib import admin
from .models import Project, Task, Profile


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "manager",
        "priority",
        "status",
        "deadline",
        "created_at",
    )
    search_fields = ("name", "manager", "tags")
    list_filter = ("priority", "status", "deadline")
    ordering = ("-created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "project",
        "assignee",
        "status",
        "deadline",
        "created_at",
    )
    search_fields = ("name", "assignee", "tags")
    list_filter = ("status", "deadline")
    ordering = ("-created_at",)
    autocomplete_fields = ("project",)  # ✅ dropdown instead of typing project id


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "bio", "image")
    search_fields = ("user__username", "user__email", "bio")
    autocomplete_fields = ("user",)
