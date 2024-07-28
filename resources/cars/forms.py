from dal import autocomplete
from django import forms

from resources.cars.models import Car, CarModel


class CarForm(forms.ModelForm):
    image_file = forms.ImageField(required=False)

    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'car_model': autocomplete.ModelSelect2(url='carmodel-autocomplete', forward=['brand']),
            'body_type': autocomplete.ModelSelect2(url='bodytype-autocomplete')
        }


class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = '__all__'
        widgets = {
            'brand': autocomplete.ModelSelect2(url='brand-autocomplete')
        }
