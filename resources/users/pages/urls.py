from django.urls import path

from . import views

urlpatterns = [
	path("register/", views.register_view, name="page_register"),
	path("login/", views.login_view, name="page_login"),
	path("logout/", views.logout_view, name="page_logout"),
]
