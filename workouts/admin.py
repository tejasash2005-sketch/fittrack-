from django.contrib import admin
from .models import Exercise, WorkoutSession, WorkoutExercise, WorkoutPlan, PersonalRecord, WorkoutStreak

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'primary_muscle', 'difficulty', 'calories_per_minute']
    list_filter = ['category', 'primary_muscle', 'difficulty']
    search_fields = ['name']

@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'date', 'duration_minutes', 'total_calories_burned']
    list_filter = ['date']
    search_fields = ['user__username', 'name']

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'duration_weeks', 'days_per_week', 'is_active']

admin.site.register(WorkoutExercise)
admin.site.register(PersonalRecord)
admin.site.register(WorkoutStreak)
