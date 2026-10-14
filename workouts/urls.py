from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.workout_list, name='list'),
    path('log/', views.workout_log, name='log'),
    path('<int:pk>/', views.workout_detail, name='detail'),
    path('<int:pk>/delete/', views.workout_delete, name='delete'),
    path('exercises/', views.exercises_view, name='exercises'),
    path('plans/', views.plans_view, name='plans'),
    path('records/', views.personal_records, name='records'),
    path('calendar/', views.workout_calendar, name='calendar'),
]
