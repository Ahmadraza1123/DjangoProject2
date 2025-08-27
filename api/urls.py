from django.urls import path, include
from rest_framework import routers

from .views import blogViewSet,commentListCreatedView

router = routers.DefaultRouter()
router.register('blog', blogViewSet)

urlpatterns = [
    path('blog/', include(router.urls)),
    path("blogs/<int:blog_id>/comments/", commentListCreatedView.as_view()),
]