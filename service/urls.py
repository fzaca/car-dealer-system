from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path("admin/", admin.site.urls),
	# Core
    path("", include("resources.core.pages.urls")),
	# Users
	path("api/users/", include("resources.users.api.urls")),
	path("users/", include("resources.users.pages.urls")),
	# Cars
	path("api/cars/", include("resources.cars.api.urls")),
	path("cars/", include("resources.cars.pages.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
