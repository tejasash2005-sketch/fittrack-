from django.urls import path
from . import views

app_name = 'diet'

urlpatterns = [
    path('', views.diet_dashboard, name='dashboard'),
    path('add/', views.add_meal, name='add_meal'),
    path('delete/<int:pk>/', views.delete_meal, name='delete_meal'),
    path('water/add/', views.add_water, name='add_water'),
    path('food/search/', views.food_search, name='food_search'),
    path('food/database/', views.food_database, name='food_database'),
    path('meal-plans/', views.meal_plans, name='meal_plans'),
    path('goals/', views.nutrition_goals, name='goals'),
]
