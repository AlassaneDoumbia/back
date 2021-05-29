from django.urls import path
from sai import views

urlpatterns = [
    path('Pdp_in/', views.),
    path('Pdp_out/', views.),
]