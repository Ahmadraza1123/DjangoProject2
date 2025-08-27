from django.urls import path, include
from rest_framework import routers
from .views import BlogViewSet,CommentListCreatedView,ReigsterUser
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('blog', BlogViewSet)

urlpatterns = [

    path('Register/', ReigsterUser.as_view()),
    path('login/', obtain_auth_token,),
    path('blog/', include(router.urls)),
    path("blogs/<blog_id>/comments/", CommentListCreatedView.as_view()),

]