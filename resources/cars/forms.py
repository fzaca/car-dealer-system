from dal import autocomplete
from django import forms

from resources.cars.models import Car, CarModel, Trim


class TrimForm(forms.ModelForm):
    class Meta:
        model = Trim
        fields = '__all__'
        widgets = {
            'car_model': autocomplete.ModelSelect2(url='carmodel-autocomplete', forward=['brand'])
        }


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'trim': autocomplete.ModelSelect2(url='trim-autocomplete', forward=['car_model'])
        }


class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = '__all__'
        widgets = {
            'brand': autocomplete.ModelSelect2(url='brand-autocomplete')
        }
