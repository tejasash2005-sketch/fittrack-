from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/api/', views.notifications_api, name='notifications_api'),
    path('settings/', views.settings_view, name='settings'),
]
