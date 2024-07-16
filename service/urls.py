from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    # Users
    path("api/users/", include("resources.users.api.urls")),
    path("users/", include("resources.users.pages.urls")),
]
