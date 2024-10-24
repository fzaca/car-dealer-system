from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandViewSet, CarModelViewSet, BodyTypeViewSet, CarViewSet, FeaturedCarViewSet

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'car-models', CarModelViewSet)
router.register(r'body-types', BodyTypeViewSet)
router.register(r'cars', CarViewSet)
router.register(r'featured-cars', FeaturedCarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
