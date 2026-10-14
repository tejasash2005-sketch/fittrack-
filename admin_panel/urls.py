from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('users/', views.user_management, name='user_management'),
    path('users/<int:pk>/', views.user_detail_admin, name='user_detail'),
    path('users/<int:pk>/premium/', views.toggle_premium, name='toggle_premium'),
    path('food/', views.food_management, name='food_management'),
    path('stats/', views.system_stats, name='system_stats'),

    # 5 New Admin Modules
    path('exercises/', views.exercise_library, name='exercise_library'),
    path('achievements/', views.achievement_manager, name='achievement_manager'),
    path('announcements/', views.announcement_manager, name='announcement_manager'),
    path('premium-analytics/', views.premium_analytics, name='premium_analytics'),
    path('system-logs/', views.system_logs, name='system_logs'),
]
