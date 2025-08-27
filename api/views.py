from rest_framework import generics, viewsets,filters
from .models import Blog,Comment
from .serializer import BlogSerializer, CommentSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.filter(published=True)
    serializer_class = BlogSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category',)

class CommentListCreatedView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        blog_id = self.kwargs['blog_id']
        return Comment.objects.filter(blog_id=blog_id)

    def perform_create(self, serializer):
        blog_id = self.kwargs['blog_id']
        serializer.save(blog_id=blog_id)

