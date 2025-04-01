import os
import string
import logging
logger = logging.getLogger(__name__)
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .utils import get_usb_key
from django.contrib import messages
from .forms import ProjectForm, BlogForm
from core.models import Project, Blog, Category
import ctypes



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session["login_success"] = f"Welcome back, {user.username}! Hope you brought snacks."
            return JsonResponse({"redirect_url": "/dashboard"})
        else:
            return JsonResponse({"error": "Wrong password? Or did your fingers slip? Try again!"}, status=400)

    # Clear success messages when user lands on login page
    if "login_success" in request.session:
        del request.session["login_success"]

    form = AuthenticationForm()
    return render(request, "vault/login.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"redirect_url": "/login"})  # Ensure JSON response

def recover_view(request):
    """Render the recovery options page without a form."""
    return render(request, "vault/recover/recover.html")

@login_required
def dashboard(request):
    success_message = request.session.pop("login_success", None)

    blogs = Blog.objects.all().order_by('-timestamp')
    categories = Category.objects.all()
    blog_form = BlogForm()

    if request.method == "POST":
        blog_form = BlogForm(request.POST, request.FILES)
        if blog_form.is_valid():
            blog_form.save()
            return redirect('dashboard')

    return render(request, "vault/dashboard.html", {
        "success_message": success_message,
        "blogs": blogs,
        "categories": categories,
        "blog_form": blog_form
    })
    
@login_required
def manage_projects(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(request.path)  # Refresh the page

    else:
        form = ProjectForm()

    projects = Project.objects.all().order_by('-created_at')
    return render(request, "manage.html", {"form": form, "projects": projects})


@login_required
def settings_view(request):
    return render(request, "vault/settings.html")

User = get_user_model()

def password_reset_with_usb(request):
    """Renders the password reset page but checks for USB key."""
    
    usb_detected = False

    if os.path.exists(USB_DRIVE_PATH):
        with open(USB_DRIVE_PATH, "r") as key_file:
            secret_key = key_file.read().strip()

        if secret_key.startswith("SecretInfinityKey-"):
            usb_detected = True  # Trigger UI changes

    if request.method == "POST":
        new_password = request.POST.get("password")
        user = request.user  

        if user.is_authenticated:
            user.set_password(new_password)
            user.save()
            login(request, user)  
            messages.success(request, "Password reset successfully!")
            return redirect("dashboard")  

    return render(request, "vault/recover/password_reset_form.html", {"usb_detected": usb_detected})

def usb_reset_request(request):
    """Checks for USB key and allows reset."""
    print("Checking USB Key...")  # Debugging line

    if os.path.exists(USB_DRIVE_PATH):
        print(f"USB Key found at {USB_DRIVE_PATH}")  # Debugging line

        with open(USB_DRIVE_PATH, "r") as key_file:
            secret_key = key_file.read().strip()
            print(f"Read Key: {secret_key}")  # Debugging line

        if secret_key.startswith("SecretInfinityKey-"):
            print("USB Key is valid! Redirecting...")
            return redirect("usb_reset_form")

    messages.error(request, "USB Key not detected or invalid.")
    print("USB Key check failed.")
    return redirect("recover")

def usb_reset_form(request):
    """Validate USB key and reset password securely."""
    
    secret_key = get_usb_key()  # Fetch key from USB
    user = User.objects.filter(usb_secret=secret_key).first()
    
    if not user:
        messages.error(request, "Invalid USB Key or User not found.")
        return redirect("recover")  # Redirect back to recovery page

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            login(request, user)  # Log in after password reset
            messages.success(request, "Password reset successfully!")
            return redirect("dashboard")

        messages.error(request, "Passwords do not match.")

    return render(request, "vault/recover/usb_reset_form.html")


@login_required
def generate_or_regenerate_usb_key(request):
    """Generate a USB key, update user info, and save it to USB if detected."""
    if request.method == "POST":
        user = request.user  
        secret_key = user.generate_usb_secret()  # 🔥 Update user's USB key

        usb_path = detect_usb_drive()  # 🔍 Detect the USB drive
        if usb_path:
            try:
                usb_file_path = os.path.join(usb_path, "infinitykey.txt")  # ✅ Save as infinitykey.txt
                with open(usb_file_path, "w") as key_file:
                    key_file.write(secret_key)
                messages.success(request, f"USB Key saved to {usb_file_path}!")
                return JsonResponse({"success": True, "message": f"USB Key saved to {usb_file_path}!"})
            except Exception as e:
                return JsonResponse({"success": False, "error": f"Error writing USB key: {str(e)}"}, status=400)
        else:
            return JsonResponse({"success": False, "error": "No USB detected. Key updated but not saved."}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# 🔍 Function to Detect USB Drive
def detect_usb_drive():
    """Detects the first available USB drive on Windows."""
    drives = [f"{d}:/" for d in string.ascii_uppercase if os.path.exists(f"{d}:/")]
    
    for drive in drives:
        try:
            drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)
            if drive_type == 2:  # 2 = DRIVE_REMOVABLE (USB)
                return drive  # ✅ Return first USB drive detected
        except Exception as e:
            print(f"Error detecting USB: {e}")

    return None  # ❌ No USB found

# Edit Project
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("manage_projects")  # Redirect to project management page
    else:
        form = ProjectForm(instance=project)

    return render(request, "edit_project.html", {"form": form, "project": project})

# Delete Project
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        project.delete()
        return redirect("manage_projects")
    return render(request, "delete_confirm.html", {"project": project})

def bulk_delete_projects(request):
    if request.method == "POST":
        project_ids = request.POST.getlist('project_ids')
        Project.objects.filter(id__in=project_ids).delete()
    return redirect('manage_projects')  # Adjust this to your actual project list URL name

def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BlogForm(instance=blog)

    return render(request, "edit_blog.html", {"form": form, "blog": blog})

def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    return redirect('dashboard')