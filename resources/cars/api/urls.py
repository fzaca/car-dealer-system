from django.urls import path

from resources.cars.api.views import BrandAutocomplete, CarModelAutocomplete


urlpatterns = [
    path('carmodel-autocomplete/', CarModelAutocomplete.as_view(), name='carmodel-autocomplete'),
    path('brand-autocomplete/', BrandAutocomplete.as_view(), name='brand-autocomplete'),
]
