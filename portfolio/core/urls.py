from django.urls import path
from .views import index, style, download_cv

urlpatterns = [
    path('', index, name='index'),
    path('style/', style, name='style'),
    path("download-cv/", download_cv, name="download_cv"),
]