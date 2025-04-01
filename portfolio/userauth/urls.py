from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import login_view, recover_view, dashboard, manage_projects, settings_view, logout_view, usb_reset_request, usb_reset_form, generate_or_regenerate_usb_key, edit_project, delete_project, bulk_delete_projects, edit_blog, delete_blog

urlpatterns = [
    path("login/", login_view, name="login"),
    path("recover/", recover_view, name="recover"),
    path("dashboard/", dashboard, name="dashboard"),
    path("manage/", manage_projects, name="manage_projects"),
    path("settings/", settings_view, name="settings"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    
    path("usb-reset/", usb_reset_request, name="usb_reset_request"),
    path("usb-reset/form/", usb_reset_form, name="usb_reset_form"),
    path("update-usb-key/", generate_or_regenerate_usb_key, name="update_usb_key"),
    path("edit/<int:project_id>/", edit_project, name="edit_project"),
    path("delete/<int:project_id>/", delete_project, name="delete_project"),
    path('bulk-delete/', bulk_delete_projects, name='bulk_delete_projects'),
    
    path('edit-blog/<int:blog_id>/', edit_blog, name="edit_blog"),
    path('delete-blog/<int:blog_id>/', delete_blog, name="delete_blog"),
    


# ✅ Adjusted Password Reset URLs to use templates inside vault/recover/
    path("password-reset/", 
         auth_views.PasswordResetView.as_view(template_name="vault/recover/password_reset_form.html"), 
         name="password_reset"),
    path("password-reset/done/", 
         auth_views.PasswordResetDoneView.as_view(template_name="vault/recover/password_reset_done.html"), 
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="vault/recover/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    path("password-reset-complete/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="vault/recover/password_reset_complete.html"), 
         name="password_reset_complete"),
]
