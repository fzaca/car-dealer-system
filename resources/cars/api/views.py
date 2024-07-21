from dal import autocomplete

from resources.cars.models import Brand, CarModel, Trim


class CarModelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CarModel.objects.none()

        queryset = CarModel.objects.all()

        if self.q:
            queryset = queryset.filter(name__icontains=self.q)

        return queryset


class TrimAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Trim.objects.none()

        queryset = Trim.objects.all()

        if self.q:
            queryset = queryset.filter(name__icontains=self.q)

        if 'car_model' in self.forwarded:
            queryset = queryset.filter(car_model=self.forwarded.get('car_model'))

        return queryset


class BrandAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Brand.objects.none()

        queryset = Brand.objects.all()

        if self.q:
            queryset = queryset.filter(name__icontains=self.q)

        return queryset
