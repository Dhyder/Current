from django.shortcuts import render
from .models import Project
from django.http import FileResponse
import os
from django.conf import settings

def index(request):
    return render(request, 'content/index.html')  # Make sure the path matches your project structure


def style(request):
    return render(request, 'content/styles.html')  # Make sure the path matches your project structure

def download_cv(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'cv', 'test.pdf')

    if not os.path.exists(file_path):
        raise Http404("CV not found")

    return FileResponse(open(file_path, 'rb'), content_type='application/pdf', as_attachment=True, filename="test.pdf")