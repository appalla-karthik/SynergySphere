from django.db import models
from django.utils import timezone
from django.conf import settings


class Project(models.Model):
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("on-hold", "On Hold"),
    ]

    name = models.CharField(max_length=200)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    manager = models.CharField(max_length=100)
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="Medium")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="projects/", null=True, blank=True)

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="projects", blank=True
    )

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="active")
    progress = models.IntegerField(default=0)
    team_size = models.IntegerField(default=1)

    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in-progress", "In Progress"),
        ("completed", "Completed"),
    ]

    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    assignee = models.CharField(max_length=100)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    deadline = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="tasks/", null=True, blank=True)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.name} ({self.project.name})"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics/", default="default/avatar.png")

    def __str__(self):
        return self.user.username
