from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render

from resources.users.forms import UserRegisterForm, CustomAuthenticationForm
from resources.users.models import CustomUser
from resources.users.decorators import redirect_if_authenticated


@redirect_if_authenticated
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


@redirect_if_authenticated
def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username_or_email, password=password)

            if user is None:
                try:
                    user_instance = CustomUser.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_instance.username, password=password)
                except CustomUser.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid username/email or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")
