from django.urls import path

from . import views

urlpatterns = [
	path("register/", views.register_view, name="page_register"),
	path("login/", views.login_view, name="page_login"),
	path("logout/", views.logout_view, name="page_logout"),
	path("", views.user_list_view, name="page_user_list"),
	path("<int:pk>/", views.user_detail_view, name="page_user_detail"),
]
