from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date, timedelta
from accounts.models import UserProfile
from workouts.models import WorkoutSession, WorkoutStreak
from diet.models import MealEntry, WaterIntake
from metrics.models import BodyMetric, StepCount, SleepLog, MoodLog
import json
import random


# ✅ Dummy data generator
def generate_dummy_data(days):
    weight, calories, steps, sleep = [], [], [], []
    base_weight = random.randint(60, 80)

    for _ in range(len(days)):
        base_weight += random.uniform(-0.2, 0.2)
        weight.append(round(base_weight, 1))
        calories.append(random.randint(1600, 2600))
        steps.append(random.randint(2000, 12000))
        sleep.append(round(random.uniform(5.5, 8.5), 1))

    return weight, calories, steps, sleep


def landing_page(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_panel:dashboard')
        return redirect('dashboard:home')
    return render(request, 'landing.html')


@login_required
def home(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_panel:dashboard')

    today = date.today()
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    streak, _ = WorkoutStreak.objects.get_or_create(user=request.user)

    today_workouts = WorkoutSession.objects.filter(user=request.user, date=today)
    today_meals = MealEntry.objects.filter(user=request.user, date=today)
    today_water = WaterIntake.objects.filter(user=request.user, date=today)
    today_steps_obj = StepCount.objects.filter(user=request.user, date=today).first()

    total_calories_burned = sum(w.total_calories_burned for w in today_workouts)
    total_calories_consumed = sum(m.total_calories for m in today_meals)
    total_water_ml = sum(w.amount_ml for w in today_water)
    today_steps_count = today_steps_obj.steps if today_steps_obj else 0

    week_labels, week_calories, week_workouts = [], [], []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        sessions = WorkoutSession.objects.filter(user=request.user, date=d)

        week_labels.append(d.strftime('%a'))
        week_calories.append(float(sum(s.total_calories_burned for s in sessions)))
        week_workouts.append(sessions.count())

    recent_workouts = WorkoutSession.objects.filter(
        user=request.user
    ).order_by('-date')[:5]

    latest_metric = BodyMetric.objects.filter(
        user=request.user
    ).order_by('-date').first()

    month_start = today.replace(day=1)
    month_sessions = WorkoutSession.objects.filter(
        user=request.user, date__gte=month_start
    )

    month_workouts = month_sessions.count()
    month_calories = sum(w.total_calories_burned for w in month_sessions)

    today_mood = MoodLog.objects.filter(user=request.user, date=today).first()

    context = {
        'profile': profile,
        'streak': streak,
        'today': today,
        'total_calories_burned': total_calories_burned,
        'total_calories_consumed': total_calories_consumed,
        'total_water_ml': total_water_ml,
        'total_water_l': round(total_water_ml / 1000, 2),
        'today_steps_count': today_steps_count,
        'recent_workouts': recent_workouts,
        'latest_metric': latest_metric,
        'month_workouts': month_workouts,
        'month_calories': round(month_calories),
        'today_mood': today_mood,
        'week_labels': json.dumps(week_labels),
        'week_calories': json.dumps(week_calories),
        'week_workouts': json.dumps(week_workouts),
        'calorie_net': total_calories_consumed - total_calories_burned,
        'water_goal': profile.daily_water_goal * 1000,
        'steps_goal': profile.daily_steps_goal,
        'calorie_goal': profile.daily_calorie_goal,
    }

    return render(request, 'dashboard/home.html', context)


@login_required
def analytics(request):
    today = date.today()

    days_30 = [today - timedelta(days=i) for i in range(29, -1, -1)]
    labels = [d.strftime('%b %d') for d in days_30]

    weight_data, calories_data, steps_data, sleep_data = [], [], [], []
    has_real_data = False  # ✅ track real data

    for d in days_30:
        metric = BodyMetric.objects.filter(
            user=request.user,
            date__lte=d
        ).order_by('-date').first()

        meals = MealEntry.objects.filter(user=request.user, date=d)
        steps = StepCount.objects.filter(user=request.user, date=d).first()
        sleep = SleepLog.objects.filter(user=request.user, date=d).first()

        w = float(metric.weight) if metric and metric.weight else 0
        c = float(sum(m.total_calories for m in meals))
        s = steps.steps if steps else 0
        sl = float(sleep.duration_hours) if sleep else 0

        if any([w, c, s, sl]):
            has_real_data = True

        weight_data.append(w)
        calories_data.append(c)
        steps_data.append(s)
        sleep_data.append(sl)

    # ✅ If no data → generate dummy data
    if not has_real_data:
        weight_data, calories_data, steps_data, sleep_data = generate_dummy_data(days_30)

    context = {
        'labels': json.dumps(labels),
        'weight_data': json.dumps(weight_data),
        'calories_data': json.dumps(calories_data),
        'steps_data': json.dumps(steps_data),
        'sleep_data': json.dumps(sleep_data),
        'is_dummy': not has_real_data,  # 👈 optional UI flag
        'today': today,
    }

    return render(request, 'dashboard/analytics.html', context)


@login_required
def quick_log(request):
    if request.method == 'POST':
        log_type = request.POST.get('type')
        today = date.today()

        if log_type == 'water':
            amount = int(request.POST.get('amount', 250))
            WaterIntake.objects.create(
                user=request.user,
                date=today,
                amount_ml=amount
            )
            return JsonResponse({'success': True, 'message': f'+{amount}ml water logged!'})

        elif log_type == 'steps':
            steps_val = int(request.POST.get('steps', 0))
            obj, _ = StepCount.objects.get_or_create(
                user=request.user,
                date=today
            )
            obj.steps = steps_val
            obj.save()

            return JsonResponse({'success': True, 'message': f'{steps_val} steps logged!'})

        elif log_type == 'mood':
            mood = int(request.POST.get('mood', 3))
            energy = int(request.POST.get('energy', 3))

            MoodLog.objects.update_or_create(
                user=request.user,
                date=today,
                defaults={'mood': mood, 'energy': energy}
            )

            return JsonResponse({'success': True, 'message': 'Mood logged!'})

    return JsonResponse({'success': False})