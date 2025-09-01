from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog, Comment,BlogReaction,CommentReaction
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
    comment_user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'comment_user', 'content', 'created_at']
        read_only_fields = ['comment_user']

    def create(self, validated_data):
        validated_data["comment_user"] = self.context["request"].user
        return super(CommentSerializer, self).create(validated_data)


class BlogSerializer(serializers.ModelSerializer):
        comments = CommentSerializer(many=True, read_only=True)
        author = serializers.ReadOnlyField(source='author.username')


        class Meta:
           model = Blog
           fields = "__all__"
           read_only_fields = ('author', 'created_at', 'updated_at')

class BlogReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogReaction
        fields = '__all__'


class CommentReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReaction
        fields = '__all__'

























