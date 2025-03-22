from django.shortcuts import render
from .models import Project
from django.http import FileResponse
import os
from django.conf import settings

def index(request):
    recent_projects = Project.objects.order_by('-created_at')[:6]  # Fetch 6 latest projects

    for project in recent_projects:
        project.tech_list = project.technologies.split(",")  # Split technologies into a list

    return render(request, 'content/index.html', {'projects': recent_projects})



def style(request):
    return render(request, 'content/styles.html')  # Make sure the path matches your project structure

def projects(request):
    all_projects = Project.objects.all()  # Fetch all projects from the database
    return render(request, 'content/projects.html', {'projects': all_projects})

def download_cv(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'cv', 'test.pdf')

    if not os.path.exists(file_path):
        raise Http404("CV not found")

    return FileResponse(open(file_path, 'rb'), content_type='application/pdf', as_attachment=True, filename="test.pdf")