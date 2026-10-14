from django.urls import path
from . import views

app_name = 'metrics'

urlpatterns = [
    path('', views.metrics_dashboard, name='dashboard'),
    path('body/log/', views.log_body_metric, name='log_body'),
    path('steps/log/', views.log_steps, name='log_steps'),
    path('sleep/log/', views.log_sleep, name='log_sleep'),
    path('mood/log/', views.log_mood, name='log_mood'),
    path('goals/', views.health_goals, name='goals'),
    path('photos/', views.progress_photos, name='photos'),
]
