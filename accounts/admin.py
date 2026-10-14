from django.contrib import admin
from .models import UserProfile, Achievement, Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'height', 'weight', 'fitness_goal', 'is_premium']
    list_filter = ['gender', 'fitness_goal', 'is_premium', 'activity_level']
    search_fields = ['user__username', 'user__email']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'title', 'is_read', 'created_at']
    list_filter = ['type', 'is_read']
