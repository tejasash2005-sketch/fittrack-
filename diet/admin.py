from django.contrib import admin
from .models import FoodItem, MealEntry, WaterIntake, MealPlan, NutritionGoal

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'calories', 'protein', 'carbohydrates', 'fat', 'is_verified']
    list_filter = ['category', 'is_verified']
    search_fields = ['name', 'brand']

@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'food_item', 'meal_type', 'date', 'quantity']
    list_filter = ['meal_type', 'date']
    search_fields = ['user__username', 'food_item__name']

admin.site.register(WaterIntake)
admin.site.register(MealPlan)
admin.site.register(NutritionGoal)
