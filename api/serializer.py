from rest_framework import serializers
from .models import blog, comment

class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = ['id', 'comment_name', 'content', 'created_at']


class blogSerializer(serializers.ModelSerializer):
    comments = commentSerializer(many=True, read_only=True)

    class Meta:
        model = blog
        fields = [
            'id',
            'content',
            'author',
            'created_at',
            'updated_at',
            'category',
            'published',
            'comments',
        ]
