from dal import autocomplete

from resources.cars.models import Brand, CarModel


class CarModelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CarModel.objects.none()

        queryset = CarModel.objects.all()

        if self.q:
            queryset = queryset.filter(name__icontains=self.q)

        return queryset


class BrandAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Brand.objects.none()

        queryset = Brand.objects.all()

        if self.q:
            queryset = queryset.filter(name__icontains=self.q)

        return queryset
