from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from resources.cars.models import Brand, CarModel, BodyType, Car, FeaturedCar
from resources.cars.serializers import BrandSerializer, CarModelSerializer, CarSerializer
from resources.cars.serializers import BodyTypeSerializer, FeaturedCarSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing brand instances.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]


class CarModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing car models.
    """
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [permissions.AllowAny]


class BodyTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing body types.
    """
    queryset = BodyType.objects.all()
    serializer_class = BodyTypeSerializer
    permission_classes = [permissions.AllowAny]


class CarViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing cars.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def featured(self, request):
        """
        Returns a list of featured cars.
        """
        featured_cars = Car.objects.filter(is_featured=True)
        serializer = self.get_serializer(featured_cars, many=True)
        return Response(serializer.data)


class FeaturedCarViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing featured cars.
    """
    queryset = FeaturedCar.objects.select_related('car').all()
    serializer_class = FeaturedCarSerializer
    permission_classes = [permissions.AllowAny]
