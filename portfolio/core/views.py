import os
# import requests
from .models import Project, Analytics, VisitorLocation
from django.shortcuts import render
from .models import Project
from django.http import FileResponse, Http404
from django.conf import settings

def index(request):
    # Fetch latest 6 projects
    recent_projects = Project.objects.order_by('-created_at')[:6]
    for project in recent_projects:
        project.tech_list = project.technologies.split(",")

    # Track portfolio visit count
    analytics, created = Analytics.objects.get_or_create(id=1)
    analytics.increment_visits()

    # Track visitor location (if not logged in session)
    if "visitor_logged" not in request.session:
        ip = get_client_ip(request)
        location_data = get_ip_location(ip)
        if location_data:
            VisitorLocation.objects.create(ip_address=ip, city=location_data.get("city"), country=location_data.get("country"))
        request.session["visitor_logged"] = True  # Mark session to prevent duplicate logs

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

    # Track CV downloads
    analytics, created = Analytics.objects.get_or_create(id=1)
    analytics.increment_cv_downloads()

    return FileResponse(open(file_path, 'rb'), content_type='application/pdf', as_attachment=True, filename="test.pdf")

def get_client_ip(request):
    """Retrieve client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def get_ip_location(ip):
    """Fetch location data from IP using an API"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return {"city": data.get("city"), "country": data.get("country")}
    except:
        return None