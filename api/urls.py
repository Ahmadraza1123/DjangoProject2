from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, CommentListCreatedView, RegisterUser, LoginCreated

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)

urlpatterns = [
    path('Register/', RegisterUser.as_view(), name='Register'),
    path('login/', LoginCreated.as_view(), name='login'),
    path('blogs/<int:blog_id>/comments/', CommentListCreatedView.as_view(), name='comments'),
    path('', include(router.urls)),
]
