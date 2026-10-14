from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg
from datetime import date, timedelta
from accounts.models import UserProfile, Achievement
from workouts.models import WorkoutSession
from diet.models import MealEntry, FoodItem
from metrics.models import BodyMetric


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


@login_required
@user_passes_test(is_admin, login_url='/dashboard/')
def admin_dashboard(request):
    today = date.today()
    total_users = User.objects.count()
    active_today = WorkoutSession.objects.filter(date=today).values('user').distinct().count()
    new_this_week = User.objects.filter(date_joined__gte=today - timedelta(days=7)).count()
    total_workouts = WorkoutSession.objects.count()
    total_meals = MealEntry.objects.count()
    premium_users = UserProfile.objects.filter(is_premium=True).count()

    recent_users = User.objects.order_by('-date_joined')[:10]
    recent_workouts = WorkoutSession.objects.select_related('user').order_by('-date')[:10]

    # Weekly signups
    week_signups = []
    week_labels = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        week_signups.append(User.objects.filter(date_joined__date=d).count())
        week_labels.append(d.strftime('%a'))

    # Workout activity per day
    week_workouts = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        week_workouts.append(WorkoutSession.objects.filter(date=d).count())

    import json
    context = {
        'total_users': total_users,
        'active_today': active_today,
        'new_this_week': new_this_week,
        'total_workouts': total_workouts,
        'total_meals': total_meals,
        'premium_users': premium_users,
        'recent_users': recent_users,
        'recent_workouts': recent_workouts,
        'week_labels': json.dumps(week_labels),
        'week_signups': json.dumps(week_signups),
        'week_workouts': json.dumps(week_workouts),
        'today': today,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def user_management(request):
    users = User.objects.select_related('profile').order_by('-date_joined')
    search = request.GET.get('search', '')
    if search:
        users = users.filter(username__icontains=search) | users.filter(email__icontains=search)
    return render(request, 'admin_panel/users.html', {'users': users, 'search': search})


@login_required
@user_passes_test(is_admin)
def user_detail_admin(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    workouts = WorkoutSession.objects.filter(user=user).order_by('-date')[:10]
    meals = MealEntry.objects.filter(user=user).order_by('-date')[:10]
    return render(request, 'admin_panel/user_detail.html', {
        'target_user': user, 'profile': profile,
        'workouts': workouts, 'meals': meals
    })


@login_required
@user_passes_test(is_admin)
def toggle_premium(request, pk):
    profile = get_object_or_404(UserProfile, user_id=pk)
    profile.is_premium = not profile.is_premium
    profile.save()
    return redirect('admin_panel:user_management')


@login_required
@user_passes_test(is_admin)
def food_management(request):
    foods = FoodItem.objects.all().order_by('-id')
    if request.method == 'POST':
        FoodItem.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category', 'other'),
            serving_size=float(request.POST.get('serving_size', 100)),
            calories=float(request.POST.get('calories', 0)),
            protein=float(request.POST.get('protein', 0)),
            carbohydrates=float(request.POST.get('carbs', 0)),
            fat=float(request.POST.get('fat', 0)),
            is_verified=True,
            created_by=request.user,
        )
        from django.contrib import messages
        messages.success(request, 'Food item added!')
        return redirect('admin_panel:food_management')
    return render(request, 'admin_panel/food_management.html', {'foods': foods})


@login_required
@user_passes_test(is_admin)
def system_stats(request):
    from workouts.models import Exercise
    context = {
        'total_users': User.objects.count(),
        'total_exercises': Exercise.objects.count(),
        'total_foods': FoodItem.objects.count(),
        'total_workouts': WorkoutSession.objects.count(),
        'total_meals': MealEntry.objects.count(),
        'avg_workouts_per_user': WorkoutSession.objects.count() / max(User.objects.count(), 1),
    }
    return render(request, 'admin_panel/stats.html', context)


@login_required
@user_passes_test(is_admin)
def exercise_library(request):
    from workouts.models import Exercise
    exercises = Exercise.objects.all().order_by('name')
    return render(request, 'admin_panel/exercises.html', {'exercises': exercises})


@login_required
@user_passes_test(is_admin)
def achievement_manager(request):
    achievements = Achievement.objects.all().order_by('points')
    return render(request, 'admin_panel/achievements.html', {'achievements': achievements})


@login_required
@user_passes_test(is_admin)
def announcement_manager(request):
    # Simulated announcements
    announcements = [
        {'id': 1, 'title': 'Maintenance Scheduled', 'date': '2024-06-01', 'status': 'Draft'},
        {'id': 2, 'title': 'New HIIT Exercises Added', 'date': '2024-05-15', 'status': 'Published'},
    ]
    return render(request, 'admin_panel/announcements.html', {'announcements': announcements})


@login_required
@user_passes_test(is_admin)
def premium_analytics(request):
    total_users = User.objects.count()
    premium_users = UserProfile.objects.filter(is_premium=True).count()
    conversion_rate = (premium_users / total_users * 100) if total_users > 0 else 0

    context = {
        'total_users': total_users,
        'premium_users': premium_users,
        'conversion_rate': round(conversion_rate, 1),
        'estimated_revenue': premium_users * 9.99,  # $9.99 per premium user
    }
    return render(request, 'admin_panel/premium_analytics.html', context)


@login_required
@user_passes_test(is_admin)
def system_logs(request):
    # Simulated logs
    logs = [
        {'time': '2024-05-20 10:30', 'user': 'admin', 'action': 'Login Success', 'ip': '192.168.1.1'},
        {'time': '2024-05-20 11:15', 'user': 'demo', 'action': 'Workout Logged', 'ip': '192.168.1.5'},
        {'time': '2024-05-20 12:00', 'user': 'admin', 'action': 'Created Food Item', 'ip': '192.168.1.1'},
    ]
    return render(request, 'admin_panel/logs.html', {'logs': logs})
