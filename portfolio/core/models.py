from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    technologies = models.CharField(max_length=255, default="Not specified", help_text="Comma-separated values (e.g. Django, React, PostgreSQL)")
    project_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)  # <-- Add this
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
