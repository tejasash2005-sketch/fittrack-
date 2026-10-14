from django.contrib import admin
from .models import BodyMetric, StepCount, SleepLog, MoodLog, HealthGoal

@admin.register(BodyMetric)
class BodyMetricAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'weight', 'body_fat_percentage', 'resting_heart_rate']
    list_filter = ['date']
    search_fields = ['user__username']

@admin.register(StepCount)
class StepCountAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'steps', 'distance_km', 'calories_burned']

@admin.register(SleepLog)
class SleepLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'duration_hours', 'quality']

admin.site.register(MoodLog)
admin.site.register(HealthGoal)
