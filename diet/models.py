from django.db import models
from django.contrib.auth.models import User


class FoodItem(models.Model):
    CATEGORY_CHOICES = [
        ('protein', 'Protein'), ('carbs', 'Carbohydrates'), ('fats', 'Healthy Fats'),
        ('vegetables', 'Vegetables'), ('fruits', 'Fruits'), ('dairy', 'Dairy'),
        ('grains', 'Grains'), ('snacks', 'Snacks'), ('beverages', 'Beverages'), ('other', 'Other'),
    ]
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    serving_size = models.FloatField(default=100, help_text='grams')
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0, help_text='grams')
    carbohydrates = models.FloatField(default=0, help_text='grams')
    fat = models.FloatField(default=0, help_text='grams')
    fiber = models.FloatField(default=0, help_text='grams')
    sugar = models.FloatField(default=0, help_text='grams')
    sodium = models.FloatField(default=0, help_text='mg')
    vitamin_c = models.FloatField(default=0, help_text='mg')
    calcium = models.FloatField(default=0, help_text='mg')
    iron = models.FloatField(default=0, help_text='mg')
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='food/', null=True, blank=True)

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_calories = models.IntegerField(default=2000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class MealEntry(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'),
        ('snack', 'Snack'), ('pre_workout', 'Pre-Workout'), ('post_workout', 'Post-Workout'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_entries')
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.SET_NULL, null=True, blank=True)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, default='lunch')
    date = models.DateField()
    quantity = models.FloatField(default=1, help_text='Number of servings')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'meal_type']

    @property
    def total_calories(self):
        return round(self.food_item.calories * self.quantity, 1)

    @property
    def total_protein(self):
        return round(self.food_item.protein * self.quantity, 1)

    @property
    def total_carbs(self):
        return round(self.food_item.carbohydrates * self.quantity, 1)

    @property
    def total_fat(self):
        return round(self.food_item.fat * self.quantity, 1)

    def __str__(self):
        return f"{self.user.username} - {self.food_item.name} on {self.date}"


class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='water_logs')
    date = models.DateField()
    amount_ml = models.IntegerField(default=250)
    time = models.TimeField(auto_now_add=True)
    notes = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.amount_ml}ml on {self.date}"


class NutritionGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nutrition_goal')
    daily_calories = models.IntegerField(default=2000)
    daily_protein = models.FloatField(default=150)
    daily_carbs = models.FloatField(default=200)
    daily_fat = models.FloatField(default=65)
    daily_fiber = models.FloatField(default=25)
    daily_water_ml = models.IntegerField(default=2500)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Nutrition Goals"
