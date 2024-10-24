from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Documentation for API",
        contact=openapi.Contact(email="zaca03zaca@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


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
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
	urlpatterns += [
		path('__debug__/', include('debug_toolbar.urls')),
		path('silk/', include('silk.urls', namespace='silk')),
	]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
