from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta
from .models import BodyMetric, StepCount, SleepLog, MoodLog, HealthGoal
import json


@login_required
def metrics_dashboard(request):
    today = date.today()
    latest = BodyMetric.objects.filter(user=request.user).first()
    recent_metrics = BodyMetric.objects.filter(user=request.user)[:10]

    # Weight trend - last 30 days
    days = [today - timedelta(days=i) for i in range(29, -1, -1)]
    weight_labels = [d.strftime('%b %d') for d in days]
    weight_values = []
    for d in days:
        m = BodyMetric.objects.filter(user=request.user, date__lte=d).first()
        weight_values.append(float(m.weight) if m and m.weight else None)

    # Steps last 7 days
    step_labels = [d.strftime('%a') for d in reversed(days[-7:])]
    step_values = []
    for d in days[-7:]:
        s = StepCount.objects.filter(user=request.user, date=d).first()
        step_values.append(s.steps if s else 0)

    # Sleep last 7 days
    sleep_data = []
    for d in days[-7:]:
        sl = SleepLog.objects.filter(user=request.user, date=d).first()
        sleep_data.append(float(sl.duration_hours) if sl else 0)

    goals = HealthGoal.objects.filter(user=request.user, is_achieved=False)
    today_steps = StepCount.objects.filter(user=request.user, date=today).first()
    today_sleep = SleepLog.objects.filter(user=request.user, date=today).first()
    today_mood = MoodLog.objects.filter(user=request.user, date=today).first()

    context = {
        'latest': latest,
        'recent_metrics': recent_metrics,
        'weight_labels': json.dumps(weight_labels),
        'weight_values': json.dumps(weight_values),
        'step_labels': json.dumps(step_labels),
        'step_values': json.dumps(step_values),
        'sleep_data': json.dumps(sleep_data),
        'goals': goals,
        'today': today,
        'today_steps': today_steps,
        'today_sleep': today_sleep,
        'today_mood': today_mood,
    }
    return render(request, 'metrics/dashboard.html', context)


@login_required
def log_body_metric(request):
    if request.method == 'POST':

        raw_date = request.POST.get('date')

        if not raw_date:
            metric_date = date.today()
        else:
            try:
                metric_date = date.fromisoformat(raw_date)
            except ValueError:
                metric_date = date.today()

        BodyMetric.objects.create(
            user=request.user,
            date=metric_date,

            photo=request.FILES.get('photo'),

            weight=request.POST.get('weight') or None,
            body_fat_percentage=request.POST.get('body_fat') or None,
            muscle_mass=request.POST.get('muscle_mass') or None,
            waist=request.POST.get('waist') or None,
            chest=request.POST.get('chest') or None,
            hips=request.POST.get('hips') or None,
            thighs=request.POST.get('thighs') or None,
            arms=request.POST.get('arms') or None,
            resting_heart_rate=request.POST.get('resting_hr') or None,
            blood_pressure_systolic=request.POST.get('bp_sys') or None,
            blood_pressure_diastolic=request.POST.get('bp_dia') or None,
            notes=request.POST.get('notes', ''),
        )

        messages.success(request, 'Body metrics logged! 📊')
        return redirect('metrics:dashboard')

    # GET request (JUST SHOW PAGE, DO NOTHING ELSE)
    return render(request, 'metrics/log_body.html', {'today': date.today()})


@login_required
def log_steps(request):
    if request.method == 'POST':
        today = date.today()
        obj, _ = StepCount.objects.update_or_create(
            user=request.user, date=today,
            defaults={
                'steps': int(request.POST.get('steps', 0)),
                'distance_km': float(request.POST.get('distance', 0)),
                'calories_burned': float(request.POST.get('calories', 0)),
                'active_minutes': int(request.POST.get('active_minutes', 0)),
            }
        )
        messages.success(request, f'{obj.steps:,} steps logged! 👟')
        return redirect('metrics:dashboard')
    return render(request, 'metrics/log_steps.html', {'today': date.today()})


@login_required
def log_sleep(request):
    if request.method == 'POST':
        SleepLog.objects.create(
            user=request.user,
            date=request.POST.get('date', date.today()),
            sleep_time=request.POST.get('sleep_time', '22:00'),
            wake_time=request.POST.get('wake_time', '06:00'),
            duration_hours=float(request.POST.get('duration', 8)),
            quality=int(request.POST.get('quality', 3)),
            interruptions=int(request.POST.get('interruptions', 0)),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Sleep logged! 😴')
        return redirect('metrics:dashboard')
    return render(request, 'metrics/log_sleep.html', {'today': date.today()})


@login_required
def log_mood(request):
    if request.method == 'POST':
        MoodLog.objects.update_or_create(
            user=request.user, date=date.today(),
            defaults={
                'mood': int(request.POST.get('mood', 3)),
                'energy': int(request.POST.get('energy', 3)),
                'stress_level': int(request.POST.get('stress', 5)),
                'notes': request.POST.get('notes', ''),
            }
        )
        messages.success(request, 'Mood logged! 😊')
        return redirect('metrics:dashboard')
    return render(request, 'metrics/log_mood.html', {'today': date.today()})


@login_required
def health_goals(request):
    goals = HealthGoal.objects.filter(user=request.user)
    if request.method == 'POST':
        HealthGoal.objects.create(
            user=request.user,
            goal_type=request.POST.get('goal_type'),
            target_value=float(request.POST.get('target_value', 0)),
            current_value=float(request.POST.get('current_value', 0)),
            deadline=request.POST.get('deadline') or None,
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'New goal set! 🎯')
        return redirect('metrics:goals')
    return render(request, 'metrics/goals.html', {'goals': goals})

@login_required
def progress_photos(request):
    metrics_with_photos = BodyMetric.objects.filter(
        user=request.user,
        photo__isnull=False
    ).exclude(photo='')

    return render(request, 'metrics/progress_photos.html', {
        'metrics': metrics_with_photos
    })