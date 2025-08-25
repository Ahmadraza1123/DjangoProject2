from rest_framework import generics
from .models import blog,comment
from .serializer import blogSerializer, commentSerializer


class blogListCreatedView(generics.ListCreateAPIView):
    queryset = blog.objects.all()
    serializer_class = blogSerializer


class blogviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = blog.objects.all()
    serializer_class = blogSerializer



class commentListCreatedView(generics.ListCreateAPIView):
    queryset = comment.objects.all()
    serializer_class = commentSerializer

    def get_queryset(self):
        blog_id = self.kwargs['blog_id']
        return comment.objects.filter(blog_id=blog_id)

    def perform_create(self, serializer):
        blog_id = self.kwargs['blog_id']
        serializer.save(blog_id=blog_id)

