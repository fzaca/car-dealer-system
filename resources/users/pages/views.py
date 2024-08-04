from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from resources.users.forms import CustomUserCreationForm
from resources.users.models import Customer, CustomUser  # noqa: F401


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True
            user.save()
            Customer.objects.create(user=user)
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect("home")
	return render(request, "login.html")


def logout_view(request):
	logout(request)
	return redirect("home")
