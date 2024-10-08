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
	# Sales
	path("api/sales/", include("resources.sales.api.urls")),
	path("sales/", include("resources.sales.pages.urls")),
	# Reviews
	path("api/reviews/", include("resources.reviews.api.urls")),
	path("reviews/", include("resources.reviews.pages.urls")),
]

if settings.DEBUG:
	urlpatterns += [
		path('__debug__/', include('debug_toolbar.urls')),
		path('silk/', include('silk.urls', namespace='silk')),
	]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
