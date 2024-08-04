from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from resources.users.forms import UserRegisterForm
from resources.users.models import Customer, CustomUser  # noqa: F401


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_customer = True
            user.is_employee = False
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")
