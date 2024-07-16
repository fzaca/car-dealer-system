from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="api-login"),
    path("logout/", views.LogoutAPIView.as_view(), name="api-logout"),
]
