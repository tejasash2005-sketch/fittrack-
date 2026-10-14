from django.db import models
from django.contrib.auth.models import User


class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('cardio', 'Cardio'),
        ('strength', 'Strength'),
        ('flexibility', 'Flexibility'),
        ('balance', 'Balance'),
        ('hiit', 'HIIT'),
        ('yoga', 'Yoga'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]
    MUSCLE_CHOICES = [
        ('chest', 'Chest'), ('back', 'Back'), ('shoulders', 'Shoulders'),
        ('biceps', 'Biceps'), ('triceps', 'Triceps'), ('forearms', 'Forearms'),
        ('core', 'Core'), ('legs', 'Legs'), ('glutes', 'Glutes'),
        ('calves', 'Calves'), ('full_body', 'Full Body'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    primary_muscle = models.CharField(max_length=20, choices=MUSCLE_CHOICES)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    calories_per_minute = models.FloatField(default=5.0)
    difficulty = models.IntegerField(default=3, help_text='1=Easy, 5=Hard')
    equipment = models.CharField(max_length=200, blank=True)
    video_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='exercises/', null=True, blank=True)
    is_custom = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_plans')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    goal = models.CharField(max_length=100, blank=True)
    duration_weeks = models.IntegerField(default=4)
    days_per_week = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_sessions')
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, default='Workout Session')
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)
    total_calories_burned = models.FloatField(default=0)
    notes = models.TextField(blank=True)
    mood_before = models.IntegerField(default=5, help_text='1-10')
    mood_after = models.IntegerField(default=7, help_text='1-10')
    perceived_effort = models.IntegerField(default=5, help_text='1-10 RPE')
    heart_rate_avg = models.IntegerField(null=True, blank=True)
    heart_rate_max = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_completed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name} on {self.date}"


class WorkoutExercise(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(default=3)
    reps = models.IntegerField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    distance_km = models.FloatField(null=True, blank=True)
    calories_burned = models.FloatField(default=0)
    rest_seconds = models.IntegerField(default=60)
    notes = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps}"


class PersonalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personal_records')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    value = models.FloatField()
    unit = models.CharField(max_length=20, default='kg')
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name}: {self.value}{self.unit}"


class WorkoutStreak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_workout_date = models.DateField(null=True, blank=True)
    total_workouts = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.current_streak} days"
