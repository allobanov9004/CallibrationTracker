from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('create/', views.device_create, name='device_create'),
    path('<int:pk>/', views.device_detail, name='device_detail'),
    path('<int:pk>/update/', views.device_update, name='device_update'),
    path('<int:pk>/delete/', views.device_delete, name='device_delete'),
]
