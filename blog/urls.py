from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, CommentListCreatedView, RegisterUser, LoginCreated, BlogReactionView, CommentReactionView

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)

urlpatterns = [
    path('Register/', RegisterUser.as_view(), name='Register'),
    path('login/', LoginCreated.as_view(), name='login'),
    path('blogs/<int:blog_id>/comments/', CommentListCreatedView.as_view(), name='comments'),

    path("blogs/<int:blog_id>/react/", BlogReactionView.as_view(), name="blog-react"),
    path("comments/<int:comment_id>/react/", CommentReactionView.as_view(), name="comment-react"),
    path('', include(router.urls)),
]
