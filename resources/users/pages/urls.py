from django.urls import path

from . import views

urlpatterns = [
	path("login/", views.login_view, name="page-login"),
	path("logout/", views.logout_view, name="page-logout"),
]
