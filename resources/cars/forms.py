from django import forms

from resources.cars.models import Car, CarModel


class CarForm(forms.ModelForm):
    image_file = forms.ImageField(required=False)

    class Meta:
        model = Car
        fields = '__all__'


class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = '__all__'
