from rest_framework import generics, viewsets,filters ,status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Blog, Comment, User
from .serializer import BlogSerializer, CommentSerializer,UserSerializer


class ReigsterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.filter(published=True)
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category',)

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CommentListCreatedView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        blog_id = self.kwargs['blog_id']
        return Comment.objects.filter(blog_id=blog_id)

    def perform_create(self, serializer):
        blog_id = self.kwargs['blog_id']
        serializer.save(blog_id=blog_id)

