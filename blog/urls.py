from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, CommentListCreatedView, RegisterUser, LoginViewSet,LikeCreateView, DisLikeCreateView


router = DefaultRouter()
router.register(r'blogs', BlogViewSet)

urlpatterns = [
    path('Register/', RegisterUser.as_view(), name='Register'),
    path('login/', LoginViewSet.as_view(), name='login'),


    path("blogs/<int:id>/like/", LikeCreateView.as_view(), {"obj_type": "blog"}, name="like-blog"),
    path("blogs/<int:id>/dislike/", DisLikeCreateView.as_view(), {"obj_type": "blog"}, name="dislike-blog"),


    path("comments/<int:id>/like/", LikeCreateView.as_view(), {"obj_type": "comment"}, name="like-comment"),
    path("comments/<int:id>/dislike/", DisLikeCreateView.as_view(), {"obj_type": "comment"}, name="dislike-comment"),


    path('blogs/<int:blog_id>/comments/', CommentListCreatedView.as_view(), name='comments'),

    path('', include(router.urls)),
]
