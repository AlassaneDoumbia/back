from django.urls import path
from bearer import views

urlpatterns = [
    path('bearer/', views.Bearer_list),
    path('bearer/<pk>', views.Bearer_time_list),
    path('importBearer/', views.import_Bearer),
]