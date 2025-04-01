from django.db import models
from django.utils.timezone import now

class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    technologies = models.CharField(max_length=255, default="Not specified", help_text="Comma-separated values (e.g. Django, React, PostgreSQL)")
    project_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)  # <-- Add this
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
    
class Analytics(models.Model):
    page_visits = models.IntegerField(default=0)  # Portfolio visits
    cv_downloads = models.IntegerField(default=0)  # CV downloads
    last_updated = models.DateTimeField(auto_now=True)

    def increment_visits(self):
        self.page_visits += 1
        self.save()

    def increment_cv_downloads(self):
        self.cv_downloads += 1
        self.save()

class VisitorLocation(models.Model):
    ip_address = models.GenericIPAddressField()
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.city}, {self.country} ({self.ip_address})"