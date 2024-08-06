from rest_framework import serializers
from resources.reviews.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'car', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user', 'car', 'created_at', 'updated_at']
