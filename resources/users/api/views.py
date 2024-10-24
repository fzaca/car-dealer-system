from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from resources.users.models import Customer
from resources.users.serializers import CustomerSerializer


class IsStaffPermission(permissions.BasePermission):
    """
    Custom permission to only allow staff users to create customers.
    """
    def has_permission(self, request, view):
        return request.user.is_staff


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows staff to create customers.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffPermission]

    def create(self, request, *args, **kwargs):
        """
        Create a new customer. Only staff users can perform this action.
        """
        if not request.user.is_staff:
            return Response({'error': 'Only staff can create customers.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()
