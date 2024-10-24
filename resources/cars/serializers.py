from rest_framework import serializers
from .models import Brand, CarModel, BodyType, Car, FeaturedCar


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'created_at', 'updated_at']


class CarModelSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = CarModel
        fields = ['hash', 'brand', 'name', 'created_at', 'updated_at']


class BodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyType
        fields = ['id', 'name', 'created_at', 'updated_at']


class CarSerializer(serializers.ModelSerializer):
    car_model = CarModelSerializer()
    body_type = BodyTypeSerializer()

    class Meta:
        model = Car
        fields = [
            'hash', 'car_model', 'body_type', 'price', 'engine_size', 'image_url',
            'gearbox', 'fuel_type', 'color', 'year', 'mileage', 'seats', 'doors',
            'is_available', 'is_featured', 'created_at', 'updated_at'
        ]


class FeaturedCarSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = FeaturedCar
        fields = ['car', 'featured_date', 'updated_at']
