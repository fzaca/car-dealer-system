from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.http import Http404

from resources.reviews.models import Comment
from resources.reviews.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting comments associated with cars.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """
        Create a new comment associated with a specific car.

        Parameters:
        - car (int): ID of the car associated with the comment (required).

        Returns:
        - 201: Comment created successfully.
        - 400: Bad request if car ID is not provided.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car_id = request.data.get('car')
        if not car_id:
            return Response({'error': 'Car ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user, car_id=car_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Optionally filters the returned comments by a specific car ID.

        Query Parameters:
        - car (int): ID of the car to filter comments by.

        Returns:
        - List of comments filtered by the car ID.
        """
        car_id = self.request.query_params.get('car')
        return Comment.objects.filter(car__id=car_id).select_related('user').order_by('-created_at')

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_comment(self, request, pk=None):
        """
        Partially update an existing comment.

        Only the owner of the comment or a staff member can update it.

        Parameters:
        - pk (int): ID of the comment to be updated.

        Returns:
        - 200: Comment updated successfully.
        - 403: Forbidden if the user is not the owner or a staff member.
        - 404: Not found if the comment does not exist.
        """
        comment = self.get_object()
        if comment.user != request.user and not request.user.is_staff:
            return Response({"error": "You do not have permission to edit this comment."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def delete_comment(self, request, pk=None):
        """
        Delete a specific comment.

        Only the owner of the comment or a staff member can delete it.

        Parameters:
        - pk (int): ID of the comment to be deleted.

        Returns:
        - 200: Comment deleted successfully.
        - 403: Forbidden if the user is not the owner or a staff member.
        - 404: Not found if the comment does not exist.
        """
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            raise Http404("No Comment matches the given query.")  # noqa: B904

        if comment.user != request.user and not request.user.is_staff:
            return Response({"error": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_200_OK)
