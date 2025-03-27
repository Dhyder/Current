import os
import logging
logger = logging.getLogger(__name__)
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .utils import get_usb_key
from django.contrib import messages



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
        return JsonResponse({"redirect_url": "/login"})  # Ensure proper response
    return JsonResponse({"error": "Invalid request"}, status=400)

def recover_view(request):
    """Render the recovery options page without a form."""
    return render(request, "vault/recover/recover.html")

@login_required
def dashboard(request):
    success_message = request.session.pop("login_success", None)  # Get message only once
    return render(request, "vault/dashboard.html", {"success_message": success_message})


    return render(request, "vault/dashboard.html", {"success_message": success_message})

    return render(request, "vault/dashboard.html", {"success_message": success_message})
@login_required
def manage_projects(request):
    return render(request, "vault/manage.html")

@login_required
def settings_view(request):
    return render(request, "vault/settings.html")

# Define USB Key Path (Change drive letter if needed)
USB_DRIVE_PATH = "E:/infinitykey.txt"

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



def detect_usb_drive():
    """Detect the first available USB drive automatically (Windows only for now)."""
    possible_drives = ["D:/", "E:/", "F:/", "G:/", "H:/"]  # Extend this if needed
    for drive in possible_drives:
        if os.path.exists(drive):
            return os.path.join(drive, "infinitykey.txt")
    return None  # No USB found

@login_required
def generate_or_regenerate_usb_key(request):
    """Generate a new USB secret, update the user, and save to USB if detected."""
    user = request.user  
    secret_key = user.generate_usb_secret()  # 🔥 Always update the user key

    usb_path = detect_usb_drive()  # Detect available USB
    if usb_path:
        try:
            with open(usb_path, "w") as key_file:
                key_file.write(secret_key)
            messages.success(request, f"USB Key updated and saved to {usb_path}!")
        except Exception as e:
            messages.error(request, f"Failed to write USB key: {e}")
    else:
        messages.warning(request, "USB not detected. Key updated but not saved.")

    return redirect("settings")