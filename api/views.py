from rest_framework import generics, viewsets,filters
from .models import blog,comment
from .serializer import blogSerializer, commentSerializer


class blogViewSet(viewsets.ModelViewSet):
    queryset = blog.objects.filter(published=True)
    serializer_class = blogSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category',)

class commentListCreatedView(generics.ListCreateAPIView):
    queryset = comment.objects.all()
    serializer_class = commentSerializer

    def get_queryset(self):
        blog_id = self.kwargs['blog_id']
        return comment.objects.filter(blog_id=blog_id)

    def perform_create(self, serializer):
        blog_id = self.kwargs['blog_id']
        serializer.save(blog_id=blog_id)

