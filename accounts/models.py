from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly Active'),
        ('moderate', 'Moderately Active'),
        ('active', 'Very Active'),
        ('extra', 'Extra Active'),
    ]
    GOAL_CHOICES = [
        ('lose', 'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain', 'Gain Muscle'),
        ('endurance', 'Build Endurance'),
        ('flexibility', 'Improve Flexibility'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    height = models.FloatField(null=True, blank=True, help_text='Height in cm')
    weight = models.FloatField(null=True, blank=True, help_text='Weight in kg')
    target_weight = models.FloatField(null=True, blank=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='moderate')
    fitness_goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='maintain')
    daily_calorie_goal = models.IntegerField(default=2000)
    daily_water_goal = models.FloatField(default=2.5, help_text='Liters per day')
    daily_steps_goal = models.IntegerField(default=10000)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_premium = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def bmi(self):
        if self.height and self.weight:
            h = self.height / 100
            return round(self.weight / (h * h), 1)
        return None

    @property
    def bmi_category(self):
        bmi = self.bmi
        if bmi is None:
            return 'Unknown'
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        elif bmi < 30:
            return 'Overweight'
        return 'Obese'

    @property
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            b = self.date_of_birth
            return today.year - b.year - ((today.month, today.day) < (b.month, b.day))
        return None

    @property
    def tdee(self):
        """Total Daily Energy Expenditure"""
        if not all([self.height, self.weight, self.date_of_birth, self.gender]):
            return self.daily_calorie_goal
        age = self.age
        if self.gender == 'M':
            bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * age)
        multipliers = {'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'extra': 1.9}
        return round(bmr * multipliers.get(self.activity_level, 1.55))


class Achievement(models.Model):
    BADGE_CHOICES = [
        ('first_workout', '🏋️ First Workout'),
        ('week_streak', '🔥 Week Streak'),
        ('month_streak', '⚡ Month Streak'),
        ('weight_goal', '🎯 Weight Goal'),
        ('10k_steps', '👟 10K Steps'),
        ('100_workouts', '💪 100 Workouts'),
        ('water_hero', '💧 Water Hero'),
        ('calorie_master', '🥗 Calorie Master'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    badge = models.CharField(max_length=50, choices=BADGE_CHOICES)
    earned_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'badge']

    def __str__(self):
        return f"{self.user.username} - {self.badge}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('achievement', 'Achievement'),
        ('reminder', 'Reminder'),
        ('goal', 'Goal'),
        ('system', 'System'),
        ('social', 'Social'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"
