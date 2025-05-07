from django.urls import path
from django.contrib.auth import views as auth_views
from notifications import views as notification_views
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='device_list'), name='logout'),
    path('notifications/', notification_views.notifications_list, name='notifications_list'),
] 