from rest_framework import serializers
from resources.users.models import CustomUser, Customer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']


class CustomerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'phone', 'address', 'dni']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create(**user_data, is_customer=True)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
