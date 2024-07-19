from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path("admin/", admin.site.urls),
	# Core
    path('', include('resources.core.pages.urls')),
	# Users
	path("api/users/", include("resources.users.api.urls")),
	path("users/", include("resources.users.pages.urls")),
]
