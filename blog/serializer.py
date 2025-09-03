from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog, Comment, Like, DisLike


#
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    comment_user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'comment_user', 'content', 'created_at', 'likes_count', 'dislikes_count']
        read_only_fields = ['comment_user']

    def create(self, validated_data):
        validated_data["comment_user"] = self.context["request"].user
        return super().create(validated_data)

    def get_likes_count(self, obj):
        return Like.objects.filter(comment=obj).count()

    def get_dislikes_count(self, obj):
        return DisLike.objects.filter(comment=obj).count()


# Blog Serializer
class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'content', 'author',
            'created_at', 'updated_at',
            'category', 'published',
            'likes_count', 'dislikes_count',
            'comments'
        ]
        read_only_fields = ['author']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

    def get_likes_count(self, obj):
        return Like.objects.filter(blog=obj).count()

    def get_dislikes_count(self, obj):
        return DisLike.objects.filter(blog=obj).count()


# Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'blog', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']


# DisLike Serializer
class DisLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ['id', 'user', 'blog', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']
