from django.urls import path

from resources.cars.api.views import BrandAutocomplete, CarModelAutocomplete
from resources.cars.api.views import TrimAutocomplete


urlpatterns = [
    path('carmodel-autocomplete/', CarModelAutocomplete.as_view(), name='carmodel-autocomplete'),
    path('trim-autocomplete/', TrimAutocomplete.as_view(), name='trim-autocomplete'),
    path('brand-autocomplete/', BrandAutocomplete.as_view(), name='brand-autocomplete'),
]
