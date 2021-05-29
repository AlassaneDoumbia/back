from django.urls import path
from .views import FileView, FileDetail

urlpatterns = [
    path('upload/', FileView.as_view()),
    path('upload/<int:pk>/', FileDetail.as_view()),
]