from django.db import models

class Project(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    name = models.CharField(max_length=200)
    tags = models.CharField(max_length=200, blank=True)
    manager = models.CharField(max_length=100)
    deadline = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    image = models.ImageField(upload_to="project_images/", blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
