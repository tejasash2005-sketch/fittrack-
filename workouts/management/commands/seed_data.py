"""
Management command to seed FitTrack with sample data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, Achievement, Notification
from workouts.models import Exercise, WorkoutSession, WorkoutStreak, PersonalRecord
from diet.models import FoodItem, NutritionGoal
from metrics.models import BodyMetric, StepCount, SleepLog, MoodLog, HealthGoal
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample exercises, foods, and demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding FitTrack database...\n')
        self.seed_exercises()
        self.seed_foods()
        self.seed_demo_user()
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!\n'))
        self.stdout.write('👤 Demo login: username=demo  password=demo1234\n')
        self.stdout.write('👑 Admin login: username=admin  password=admin1234\n')

    def seed_exercises(self):
        exercises = [
            # Strength
            ('Barbell Bench Press', 'strength', 'chest', 'Lie on bench, grip bar shoulder-width, lower to chest and press up.', 8.0, 4, 'Barbell, Bench'),
            ('Pull-Ups', 'strength', 'back', 'Hang from bar, pull until chin clears, lower slowly.', 7.0, 4, 'Pull-up bar'),
            ('Barbell Squat', 'strength', 'legs', 'Bar on upper back, squat until thighs parallel, drive up.', 9.0, 4, 'Barbell, Rack'),
            ('Deadlift', 'strength', 'back', 'Hip-hinge movement, lift bar from floor to hip height.', 10.0, 5, 'Barbell'),
            ('Overhead Press', 'strength', 'shoulders', 'Press barbell from shoulders overhead, lock out arms.', 7.5, 4, 'Barbell'),
            ('Bicep Curl', 'strength', 'biceps', 'Stand with dumbbells, curl up keeping elbows fixed.', 5.0, 2, 'Dumbbells'),
            ('Tricep Dips', 'strength', 'triceps', 'Support on parallel bars, lower and press up.', 6.0, 3, 'Dip bars'),
            ('Romanian Deadlift', 'strength', 'glutes', 'Hip hinge with soft knees, bar slides down legs.', 8.0, 3, 'Barbell'),
            ('Leg Press', 'strength', 'legs', 'Seated machine, press platform away with feet.', 7.0, 3, 'Leg press machine'),
            ('Lat Pulldown', 'strength', 'back', 'Pull bar to upper chest while seated.', 6.5, 3, 'Cable machine'),
            ('Dumbbell Lunges', 'strength', 'legs', 'Step forward into lunge, alternate legs.', 6.0, 3, 'Dumbbells'),
            ('Cable Rows', 'strength', 'back', 'Seated cable row, pull to abdomen keeping back straight.', 6.0, 3, 'Cable machine'),
            ('Incline Dumbbell Press', 'strength', 'chest', 'Press dumbbells on incline bench.', 7.0, 3, 'Dumbbells, Bench'),
            ('Face Pulls', 'strength', 'shoulders', 'Pull cable to face level, flare elbows out.', 5.0, 2, 'Cable machine'),
            ('Plank', 'strength', 'core', 'Hold body in straight line from head to heels.', 4.0, 2, 'None'),
            ('Crunches', 'strength', 'core', 'Lie on back, lift shoulders toward knees.', 4.0, 1, 'None'),
            ('Russian Twists', 'strength', 'core', 'Seated rotation with or without weight.', 5.0, 2, 'Optional weight'),
            ('Calf Raises', 'strength', 'calves', 'Rise on toes, lower slowly.', 4.0, 1, 'None/Machine'),
            # Cardio
            ('Running', 'cardio', 'full_body', 'Sustained outdoor or treadmill running.', 11.0, 3, 'None/Treadmill'),
            ('Cycling', 'cardio', 'legs', 'Stationary or outdoor cycling at moderate intensity.', 9.0, 2, 'Bike'),
            ('Jump Rope', 'cardio', 'full_body', 'Skip rope at moderate to high intensity.', 12.0, 3, 'Jump rope'),
            ('Rowing Machine', 'cardio', 'full_body', 'Full body rowing on ergometer.', 10.0, 3, 'Rowing machine'),
            ('Stair Climber', 'cardio', 'legs', 'Climb stairs on machine at steady pace.', 9.5, 3, 'Stair machine'),
            ('Elliptical', 'cardio', 'full_body', 'Low-impact full-body cardio machine.', 8.0, 2, 'Elliptical'),
            ('Swimming', 'cardio', 'full_body', 'Laps in pool, various strokes.', 9.0, 3, 'Pool'),
            ('Walking', 'cardio', 'legs', 'Brisk walking at 5-6 km/h.', 5.0, 1, 'None'),
            # HIIT
            ('Burpees', 'hiit', 'full_body', 'Jump, plank, push-up, jump-up sequence.', 12.0, 4, 'None'),
            ('Box Jumps', 'hiit', 'legs', 'Explosive jump onto raised platform.', 10.0, 4, 'Box'),
            ('Mountain Climbers', 'hiit', 'core', 'Plank position, alternate knee drives.', 10.0, 3, 'None'),
            ('Kettlebell Swings', 'hiit', 'glutes', 'Hip hinge swing with kettlebell.', 10.0, 3, 'Kettlebell'),
            ('Battle Ropes', 'hiit', 'full_body', 'Alternating rope waves for timed intervals.', 13.0, 4, 'Battle ropes'),
            ('Sprint Intervals', 'hiit', 'full_body', 'All-out sprints with rest periods.', 14.0, 5, 'None'),
            # Yoga & Flexibility
            ('Yoga Flow', 'yoga', 'full_body', 'Series of poses with breath coordination.', 3.5, 2, 'Yoga mat'),
            ('Sun Salutation', 'yoga', 'full_body', '12-step yoga sequence to warm up.', 4.0, 2, 'Yoga mat'),
            ('Hip Flexor Stretch', 'flexibility', 'legs', 'Kneeling lunge stretch targeting hip flexors.', 2.0, 1, 'None'),
            ('Foam Rolling', 'flexibility', 'full_body', 'Self-myofascial release with foam roller.', 2.5, 1, 'Foam roller'),
        ]
        created = 0
        for name, cat, muscle, desc, cal_min, diff, equip in exercises:
            _, c = Exercise.objects.get_or_create(
                name=name,
                defaults={
                    'category': cat, 'primary_muscle': muscle,
                    'description': desc, 'calories_per_minute': cal_min,
                    'difficulty': diff, 'equipment': equip,
                }
            )
            if c:
                created += 1
        self.stdout.write(f'  ✓ {created} exercises created ({Exercise.objects.count()} total)')

    def seed_foods(self):
        foods = [
            # Proteins
            ('Chicken Breast (Grilled)', 'protein', 100, 165, 31, 0, 3.6, 0, 'Generic'),
            ('Salmon Fillet', 'protein', 100, 208, 20, 0, 13, 0, 'Generic'),
            ('Eggs (Whole)', 'protein', 50, 72, 6.3, 0.4, 4.8, 0, 'Generic'),
            ('Greek Yogurt (0%)', 'protein', 100, 59, 10, 3.6, 0.4, 0, 'Chobani'),
            ('Cottage Cheese', 'protein', 100, 98, 11, 3.4, 4.3, 0, 'Generic'),
            ('Tuna (Canned)', 'protein', 100, 132, 28, 0, 1.0, 0, 'Generic'),
            ('Ground Turkey', 'protein', 100, 149, 19, 0, 8.3, 0, 'Generic'),
            ('Beef Sirloin', 'protein', 100, 207, 26, 0, 11, 0, 'Generic'),
            ('Whey Protein', 'protein', 30, 120, 24, 3, 1.5, 0, 'Generic'),
            ('Tofu (Firm)', 'protein', 100, 76, 8.1, 1.9, 4.2, 0, 'Generic'),
            ('Lentils (Cooked)', 'protein', 100, 116, 9, 20, 0.4, 0, 'Generic'),
            ('Black Beans', 'protein', 100, 132, 8.9, 23.7, 0.5, 0, 'Generic'),
            # Carbs
            ('White Rice (Cooked)', 'carbs', 100, 130, 2.7, 28, 0.3, 0, 'Generic'),
            ('Brown Rice (Cooked)', 'carbs', 100, 123, 2.7, 26, 0.9, 0, 'Generic'),
            ('Oats (Dry)', 'carbs', 40, 150, 5, 27, 2.5, 0, 'Quaker'),
            ('Sweet Potato', 'carbs', 100, 86, 1.6, 20, 0.1, 0, 'Generic'),
            ('Whole Wheat Bread', 'carbs', 30, 80, 4, 14, 1, 0, 'Generic'),
            ('Pasta (Cooked)', 'carbs', 100, 158, 5.8, 31, 0.9, 0, 'Generic'),
            ('Quinoa (Cooked)', 'carbs', 100, 120, 4.4, 22, 1.9, 0, 'Generic'),
            ('Banana', 'fruits', 118, 105, 1.3, 27, 0.4, 0, 'Generic'),
            ('Apple', 'fruits', 182, 95, 0.5, 25, 0.3, 0, 'Generic'),
            ('Blueberries', 'fruits', 100, 57, 0.7, 14, 0.3, 0, 'Generic'),
            ('Orange', 'fruits', 131, 62, 1.2, 15, 0.2, 0, 'Generic'),
            ('Strawberries', 'fruits', 100, 32, 0.7, 7.7, 0.3, 0, 'Generic'),
            ('Mango', 'fruits', 100, 60, 0.8, 15, 0.4, 0, 'Generic'),
            # Healthy Fats
            ('Avocado', 'fats', 100, 160, 2, 9, 15, 0, 'Generic'),
            ('Almonds', 'fats', 28, 161, 6, 6, 14, 0, 'Generic'),
            ('Olive Oil', 'fats', 14, 119, 0, 0, 14, 0, 'Generic'),
            ('Peanut Butter', 'fats', 32, 190, 7, 7, 16, 0, 'Jif'),
            ('Walnuts', 'fats', 28, 185, 4.3, 3.9, 18.5, 0, 'Generic'),
            # Vegetables
            ('Broccoli (Steamed)', 'vegetables', 100, 35, 2.4, 7.2, 0.4, 0, 'Generic'),
            ('Spinach (Raw)', 'vegetables', 30, 7, 0.9, 1.1, 0.1, 0, 'Generic'),
            ('Bell Pepper', 'vegetables', 100, 31, 1, 6, 0.3, 0, 'Generic'),
            ('Carrots', 'vegetables', 100, 41, 0.9, 10, 0.2, 0, 'Generic'),
            ('Cucumber', 'vegetables', 100, 16, 0.7, 3.6, 0.1, 0, 'Generic'),
            ('Kale', 'vegetables', 67, 33, 2.9, 6, 0.5, 0, 'Generic'),
            # Dairy
            ('Whole Milk', 'dairy', 240, 149, 8, 12, 8, 0, 'Generic'),
            ('Skim Milk', 'dairy', 240, 83, 8.3, 12.2, 0.2, 0, 'Generic'),
            ('Cheddar Cheese', 'dairy', 28, 113, 7, 0.4, 9.3, 0, 'Generic'),
            ('Butter', 'dairy', 14, 102, 0.1, 0, 11.5, 0, 'Generic'),
            # Snacks & Beverages
            ('Protein Bar', 'snacks', 60, 200, 20, 22, 7, 0, 'Quest'),
            ('Rice Cakes', 'snacks', 9, 35, 0.7, 7.3, 0.3, 0, 'Generic'),
            ('Dark Chocolate (85%)', 'snacks', 28, 170, 3, 10, 15, 0, 'Generic'),
            ('Coffee (Black)', 'beverages', 240, 5, 0.3, 0, 0, 0, 'Generic'),
            ('Green Tea', 'beverages', 240, 2, 0, 0, 0, 0, 'Generic'),
            ('Orange Juice', 'beverages', 240, 112, 1.7, 26, 0.5, 0, 'Tropicana'),
        ]
        created = 0
        for data in foods:
            name, cat, serving, cal, prot, carb, fat, sugar, brand = data
            _, c = FoodItem.objects.get_or_create(
                name=name,
                defaults={
                    'category': cat, 'serving_size': serving,
                    'calories': cal, 'protein': prot, 'carbohydrates': carb,
                    'fat': fat, 'sugar': sugar, 'brand': brand, 'is_verified': True,
                }
            )
            if c:
                created += 1
        self.stdout.write(f'  ✓ {created} food items created ({FoodItem.objects.count()} total)')

    def seed_demo_user(self):
        # Create admin
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={'first_name': 'Admin', 'last_name': 'User', 'email': 'admin@fittrack.com', 'is_staff': True, 'is_superuser': True}
        )
        admin.set_password('admin1234')
        admin.save()
        UserProfile.objects.get_or_create(user=admin, defaults={'height': 180, 'weight': 80, 'fitness_goal': 'maintain', 'is_premium': True})
        WorkoutStreak.objects.get_or_create(user=admin)

        # Create demo user
        demo, created = User.objects.get_or_create(
            username='demo',
            defaults={'first_name': 'Alex', 'last_name': 'Johnson', 'email': 'alex@fittrack.com'}
        )
        demo.set_password('demo1234')
        demo.save()

        from datetime import date as d
        from accounts.models import UserProfile as UP
        profile, _ = UP.objects.get_or_create(
            user=demo,
            defaults={
                'height': 175, 'weight': 78.5, 'target_weight': 72,
                'gender': 'M', 'fitness_goal': 'lose', 'activity_level': 'moderate',
                'daily_calorie_goal': 2200, 'daily_water_goal': 2.5, 'daily_steps_goal': 10000,
                'city': 'New York', 'country': 'USA', 'is_premium': True,
            }
        )
        # Set birthday separately if not set
        if not profile.date_of_birth:
            from datetime import date
            profile.date_of_birth = date(1992, 5, 14)
            profile.save()

        streak, _ = WorkoutStreak.objects.get_or_create(user=demo)

        NutritionGoal.objects.get_or_create(
            user=demo,
            defaults={'daily_calories': 2200, 'daily_protein': 160, 'daily_carbs': 240, 'daily_fat': 70, 'daily_water_ml': 2500}
        )

        if created:
            # Seed 30 days of workout history
            workout_names = ['Push Day', 'Pull Day', 'Leg Day', 'HIIT Session', 'Full Body', 'Cardio Run', 'Yoga Flow']
            for i in range(30, 0, -1):
                if random.random() > 0.3:  # 70% chance of workout
                    day = date.today() - timedelta(days=i)
                    name = random.choice(workout_names)
                    duration = random.randint(25, 75)
                    calories = random.uniform(150, 550)
                    WorkoutSession.objects.get_or_create(
                        user=demo, date=day,
                        defaults={
                            'name': name, 'duration_minutes': duration,
                            'total_calories_burned': round(calories, 1),
                            'perceived_effort': random.randint(4, 9),
                            'mood_before': random.randint(5, 9),
                            'mood_after': random.randint(6, 10),
                            'notes': 'Great session!' if random.random() > 0.5 else '',
                        }
                    )

            # Body metrics
            weight = 80.0
            for i in range(30, 0, -1):
                day = date.today() - timedelta(days=i)
                weight += random.uniform(-0.3, 0.15)
                BodyMetric.objects.get_or_create(
                    user=demo, date=day,
                    defaults={
                        'weight': round(weight, 1),
                        'body_fat_percentage': round(random.uniform(18, 22), 1),
                        'waist': round(random.uniform(84, 88), 1),
                        'resting_heart_rate': random.randint(58, 72),
                    }
                )

            # Steps
            for i in range(14, 0, -1):
                day = date.today() - timedelta(days=i)
                steps = random.randint(4000, 14000)
                StepCount.objects.get_or_create(
                    user=demo, date=day,
                    defaults={'steps': steps, 'distance_km': round(steps * 0.0007, 2), 'calories_burned': round(steps * 0.04, 1)}
                )

            # Sleep logs
            for i in range(14, 0, -1):
                day = date.today() - timedelta(days=i)
                duration = round(random.uniform(5.5, 9.0), 1)
                SleepLog.objects.get_or_create(
                    user=demo, date=day,
                    defaults={'sleep_time': '22:30', 'wake_time': '06:30', 'duration_hours': duration, 'quality': random.randint(2, 5)}
                )

            # Mood logs
            for i in range(7, 0, -1):
                day = date.today() - timedelta(days=i)
                MoodLog.objects.get_or_create(
                    user=demo, date=day,
                    defaults={'mood': random.randint(3, 5), 'energy': random.randint(2, 5), 'stress_level': random.randint(2, 7)}
                )

            # Update streak
            streak.current_streak = 7
            streak.longest_streak = 14
            streak.total_workouts = WorkoutSession.objects.filter(user=demo).count()
            streak.last_workout_date = date.today() - timedelta(days=1)
            streak.save()

            # Goals
            HealthGoal.objects.get_or_create(user=demo, goal_type='weight', defaults={'target_value': 72, 'current_value': 78.5})
            HealthGoal.objects.get_or_create(user=demo, goal_type='steps', defaults={'target_value': 10000, 'current_value': 7500})

            # Notifications
            Notification.objects.create(user=demo, type='achievement', title='🔥 Week Streak!', message='You completed 7 workouts in a row. Keep it up!')
            Notification.objects.create(user=demo, type='goal', title='🎯 Weight Goal Progress', message='You\'re 5.5kg away from your target weight of 72kg.')
            Notification.objects.create(user=demo, type='system', title='Welcome to FitTrack!', message='Your fitness journey starts now. Log your first workout!')

            self.stdout.write(f'  ✓ Demo user "alex" seeded with 30 days of data')
        else:
            self.stdout.write(f'  ℹ Demo user already exists, skipped')
