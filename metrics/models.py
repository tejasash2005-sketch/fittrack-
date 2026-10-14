from django.db import models
from django.contrib.auth.models import User


class BodyMetric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='body_metrics')
    date = models.DateField()
    weight = models.FloatField(null=True, blank=True, help_text='kg')
    body_fat_percentage = models.FloatField(null=True, blank=True)
    muscle_mass = models.FloatField(null=True, blank=True, help_text='kg')
    waist = models.FloatField(null=True, blank=True, help_text='cm')
    chest = models.FloatField(null=True, blank=True, help_text='cm')
    hips = models.FloatField(null=True, blank=True, help_text='cm')
    thighs = models.FloatField(null=True, blank=True, help_text='cm')
    arms = models.FloatField(null=True, blank=True, help_text='cm')
    neck = models.FloatField(null=True, blank=True, help_text='cm')
    resting_heart_rate = models.IntegerField(null=True, blank=True, help_text='BPM')
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='progress_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    @property
    def bmi(self):
        if self.weight and hasattr(self.user, 'profile') and self.user.profile.height:
            h = self.user.profile.height / 100
            return round(self.weight / (h * h), 1)
        return None


class StepCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='step_counts')
    date = models.DateField()
    steps = models.IntegerField(default=0)
    distance_km = models.FloatField(default=0)
    calories_burned = models.FloatField(default=0)
    active_minutes = models.IntegerField(default=0)
    source = models.CharField(max_length=50, default='manual', help_text='manual/app/device')

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.steps} steps on {self.date}"


class SleepLog(models.Model):
    QUALITY_CHOICES = [(i, str(i)) for i in range(1, 6)]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sleep_logs')
    date = models.DateField(help_text='Date of waking up')
    sleep_time = models.TimeField()
    wake_time = models.TimeField()
    duration_hours = models.FloatField(default=0)
    quality = models.IntegerField(choices=QUALITY_CHOICES, default=3)
    deep_sleep_hours = models.FloatField(default=0)
    rem_sleep_hours = models.FloatField(default=0)
    interruptions = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.duration_hours}h sleep on {self.date}"


class MoodLog(models.Model):
    MOOD_CHOICES = [
        (1, '😢 Very Sad'), (2, '😞 Sad'), (3, '😐 Neutral'),
        (4, '😊 Happy'), (5, '😄 Very Happy'),
    ]
    ENERGY_CHOICES = [
        (1, '🪫 Exhausted'), (2, '😴 Tired'), (3, '😐 Normal'),
        (4, '⚡ Energetic'), (5, '🚀 Very Energetic'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_logs')
    date = models.DateField()
    mood = models.IntegerField(choices=MOOD_CHOICES, default=3)
    energy = models.IntegerField(choices=ENERGY_CHOICES, default=3)
    stress_level = models.IntegerField(default=5, help_text='1-10')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - Mood {self.mood} on {self.date}"


class HealthGoal(models.Model):
    GOAL_TYPE_CHOICES = [
        ('weight', 'Target Weight'), ('steps', 'Daily Steps'), ('sleep', 'Sleep Hours'),
        ('water', 'Water Intake'), ('workout', 'Workouts per Week'), ('body_fat', 'Body Fat %'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    target_value = models.FloatField()
    current_value = models.FloatField(default=0)
    deadline = models.DateField(null=True, blank=True)
    is_achieved = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.goal_type}: {self.target_value}"

    @property
    def progress_percentage(self):
        if self.target_value:
            return min(round((self.current_value / self.target_value) * 100, 1), 100)
        return 0
