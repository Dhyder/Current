from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import login_view, recover_view, dashboard, manage_projects, settings_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("recover/", recover_view, name="recover"),
    path("dashboard/", dashboard, name="dashboard"),
    path("manage/", manage_projects, name="manage"),
    path("settings/", settings_view, name="settings"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),  # ✅ Logout Added
]
