from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog, Comment
from rest_framework.authtoken.models import Token


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
    class Meta:
        model = Comment
        fields = ['id', 'comment_name', 'content', 'created_at']


class BlogSerializer(serializers.ModelSerializer):
        comments = CommentSerializer(many=True, read_only=True)
        author = serializers.ReadOnlyField(source='author.username')

        class Meta:
           model = Blog
           fields = "__all__"
           read_only_fields = ('author', 'created_at', 'updated_at')






















