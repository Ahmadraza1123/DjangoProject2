from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, filters, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Blog, Comment, Like, DisLike
from .serializer import BlogSerializer, CommentSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.filter(published=True)
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category',)


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    @action(detail=False, methods=['get'])
    def my_blogs(self, request):
        blogs = Blog.objects.filter(author=request.user)
        serializer = self.get_serializer(blogs, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        if self.action == 'list':
            return Blog.objects.filter(published=True)
        return Blog.objects.all()



class CommentListCreatedView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        blog_id = self.kwargs['blog_id']
        return Comment.objects.filter(blog_id=blog_id)

    def perform_create(self, serializer):
        blog_id = self.kwargs['blog_id']
        serializer.save(blog_id=blog_id)


class LikeCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        obj_type = self.kwargs.get("obj_type")
        obj_id = self.kwargs.get("id")

        if obj_type == "blog":
            blog = get_object_or_404(Blog, id=obj_id)


            DisLike.objects.filter(user=request.user, blog=blog).delete()


            existing_like = Like.objects.filter(user=request.user, blog=blog)
            if existing_like.exists():
                existing_like.delete()
                return Response({"message": "Removed Like from Blog"})

            like = Like.objects.create(user=request.user, blog=blog)
            return Response({"message": "Liked Blog", "id": like.id})

        elif obj_type == "comment":
            comment = get_object_or_404(Comment, id=obj_id)


            DisLike.objects.filter(user=request.user, comment=comment).delete()

            #
            existing_like = Like.objects.filter(user=request.user, comment=comment)
            if existing_like.exists():
                existing_like.delete()
                return Response({"message": "Removed Like from Comment"})

            like = Like.objects.create(user=request.user, comment=comment)
            return Response({"message": "Liked Comment", "id": like.id})

class DisLikeCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        obj_type = self.kwargs.get("obj_type")
        obj_id = self.kwargs.get("id")

        if obj_type == "blog":
            blog = get_object_or_404(Blog, id=obj_id)


            Like.objects.filter(user=request.user, blog=blog).delete()


            existing_dislike = DisLike.objects.filter(user=request.user, blog=blog)
            if existing_dislike.exists():
                existing_dislike.delete()
                return Response({"message": "Removed Dislike from Blog"})

            dislike = DisLike.objects.create(user=request.user, blog=blog)
            return Response({"message": "Disliked Blog", "id": dislike.id})

        elif obj_type == "comment":
            comment = get_object_or_404(Comment, id=obj_id)


            Like.objects.filter(user=request.user, comment=comment).delete()


            existing_dislike = DisLike.objects.filter(user=request.user, comment=comment)
            if existing_dislike.exists():
                existing_dislike.delete()
                return Response({"message": "Removed Dislike from Comment"})

            dislike = DisLike.objects.create(user=request.user, comment=comment)
            return Response({"message": "Disliked Comment", "id": dislike.id})



