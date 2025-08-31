from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, filters, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from .models import Blog, Comment
from .serializer import BlogSerializer, CommentSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginCreated(APIView):
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
