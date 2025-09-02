from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Blog, Comment, Like, DisLike


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        return user


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
        return super(CommentSerializer, self).create(validated_data)

    def get_likes_count(self, obj):
        return Like.objects.filter(comment=obj).count()

    def get_dislikes_count(self, obj):
        return DisLike.objects.filter(comment=obj).count()


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at',
                  'category', 'published', 'likes_count', 'dislikes_count', 'comments']

    def get_likes_count(self, obj):
        return Like.objects.filter(blog=obj).count()

    def get_dislikes_count(self, obj):
        return DisLike.objects.filter(blog=obj).count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'blog', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']


class DisLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ['id', 'user', 'blog', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']
