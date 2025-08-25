from django.urls import path
from .views import blogListCreatedView,blogviewDetail,commentListCreatedView

urlpatterns = [
    path('blog/', blogListCreatedView.as_view()),
    path('blog/<int:pk>/', blogviewDetail.as_view()),
    path("blogs/<int:blog_id>/comments/", commentListCreatedView.as_view()),
]