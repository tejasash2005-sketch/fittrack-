from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, timedelta
from .models import WorkoutSession, WorkoutExercise, Exercise, WorkoutPlan, PersonalRecord, WorkoutStreak
import json


@login_required
def workout_list(request):
    sessions = WorkoutSession.objects.filter(user=request.user).order_by('-date')
    streak, _ = WorkoutStreak.objects.get_or_create(user=request.user)
    total_workouts = sessions.count()
    total_calories = sum(s.total_calories_burned for s in sessions)
    total_minutes = sum(s.duration_minutes for s in sessions)
    context = {
        'sessions': sessions[:20],
        'streak': streak,
        'total_workouts': total_workouts,
        'total_calories': round(total_calories),
        'total_minutes': total_minutes,
        'total_hours': round(total_minutes / 60, 1),
    }
    return render(request, 'workouts/list.html', context)


@login_required
def workout_log(request):
    exercises = Exercise.objects.all()
    if request.method == 'POST':
        session = WorkoutSession.objects.create(
            user=request.user,
            name=request.POST.get('name', 'Workout Session'),
            date=request.POST.get('date', date.today()),
            duration_minutes=int(request.POST.get('duration', 0)),
            total_calories_burned=float(request.POST.get('calories', 0)),
            notes=request.POST.get('notes', ''),
            perceived_effort=int(request.POST.get('effort', 5)),
            mood_before=int(request.POST.get('mood_before', 5)),
            mood_after=int(request.POST.get('mood_after', 7)),
            location=request.POST.get('location', ''),
        )
        # Update streak
        streak, _ = WorkoutStreak.objects.get_or_create(user=request.user)
        streak.total_workouts += 1
        today = date.today()
        if streak.last_workout_date == today - timedelta(days=1):
            streak.current_streak += 1
        elif streak.last_workout_date != today:
            streak.current_streak = 1
        streak.last_workout_date = today
        streak.longest_streak = max(streak.longest_streak, streak.current_streak)
        streak.save()
        messages.success(request, f'Workout "{session.name}" logged successfully! 💪')
        return redirect('workouts:detail', pk=session.pk)
    return render(request, 'workouts/log.html', {'exercises': exercises, 'today': date.today()})


@login_required
def workout_detail(request, pk):
    session = get_object_or_404(WorkoutSession, pk=pk, user=request.user)
    return render(request, 'workouts/detail.html', {'session': session})


@login_required
def workout_delete(request, pk):
    session = get_object_or_404(WorkoutSession, pk=pk, user=request.user)
    if request.method == 'POST':
        session.delete()
        messages.success(request, 'Workout deleted.')
        return redirect('workouts:list')
    return render(request, 'workouts/confirm_delete.html', {'session': session})


@login_required
def exercises_view(request):
    category = request.GET.get('category', '')
    exercises = Exercise.objects.all()
    if category:
        exercises = exercises.filter(category=category)
    return render(request, 'workouts/exercises.html', {'exercises': exercises, 'category': category})


@login_required
def plans_view(request):
    plans = WorkoutPlan.objects.filter(user=request.user)
    return render(request, 'workouts/plans.html', {'plans': plans})


@login_required
def personal_records(request):
    records = PersonalRecord.objects.filter(user=request.user).select_related('exercise')
    return render(request, 'workouts/records.html', {'records': records})


@login_required
def workout_calendar(request):
    today = date.today()
    month_start = today.replace(day=1)
    sessions = WorkoutSession.objects.filter(user=request.user, date__gte=month_start)
    workout_dates = list(sessions.values_list('date', flat=True))
    workout_dates_str = [str(d) for d in workout_dates]
    return render(request, 'workouts/calendar.html', {
        'workout_dates': json.dumps(workout_dates_str),
        'today': today,
    })
