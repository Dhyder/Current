from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "vault/login.html", {"form": form})

def recover_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect("login")
    else:
        form = PasswordResetForm()
    return render(request, "vault/recover.html", {"form": form})

@login_required
def dashboard(request):
    return render(request, "vault/dashboard.html")

@login_required
def manage_projects(request):
    return render(request, "vault/manage.html")

@login_required
def settings_view(request):
    return render(request, "vault/settings.html")
