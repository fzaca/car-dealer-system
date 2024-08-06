from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from resources.reviews.models import Comment
from resources.reviews.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        car_id = self.request.query_params.get('car')
        return Comment.objects.filter(car__id=car_id).select_related('user').order_by('-created_at')

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_comment(self, request, pk=None):
        comment = self.get_object()
        if comment.user != request.user and not request.user.is_staff:
            return Response({"error": "You do not have permission to edit this comment."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def delete_comment(self, request, pk=None):
        comment = self.get_object()
        if comment.user != request.user and not request.user.is_staff:
            return Response({"error": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
