from django.urls import path, include
from rest_framework import routers

from .views import BlogViewSet,CommentListCreatedView

router = routers.DefaultRouter()
router.register('blog', BlogViewSet)

urlpatterns = [
    path('blog/', include(router.urls)),
    path("blogs/<int:blog_id>/comments/", CommentListCreatedView.as_view()),
]