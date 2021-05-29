from django.urls import path, include
from sai import views

urlpatterns = [
    path('sai_IN/', views.Sai_IN_list),
    path('sai/<int:pk>/', views.Sai_IN_detail),
    path('sai/<pk>/', views.Sai_IN_time_list),
    path('sai_out/', views.Sai_OUT_list),
    # path('sai_out/<pk>', views.Sai_OUT_time_list),
]