from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Notification
from .forms import RegisterForm, LoginForm, ProfileForm, ChangePasswordForm
from django.http import JsonResponse
import json


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome to FitTrack, {user.first_name}! Let\'s get started 🚀')
            return redirect('dashboard:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}! 💪')
            next_url = request.GET.get('next', 'dashboard:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out. See you soon! 👋')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Also update user fields
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
            messages.success(request, 'Profile updated successfully! ✅')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    achievements = request.user.achievements.all()
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile, 'achievements': achievements})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully! 🔐')
            return redirect('accounts:profile')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def notifications_view(request):
    notifs = request.user.notifications.all()
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'accounts/notifications.html', {'notifications': notifs})


@login_required
def notifications_api(request):
    notifs = request.user.notifications.filter(is_read=False)[:5]
    data = [{'title': n.title, 'message': n.message, 'type': n.type, 'time': n.created_at.strftime('%b %d')} for n in notifs]
    return JsonResponse({'count': notifs.count(), 'notifications': data})


@login_required
def settings_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.notifications_enabled = 'notifications_enabled' in request.POST
        profile.dark_mode = 'dark_mode' in request.POST
        profile.daily_calorie_goal = int(request.POST.get('daily_calorie_goal', 2000))
        profile.daily_water_goal = float(request.POST.get('daily_water_goal', 2.5))
        profile.daily_steps_goal = int(request.POST.get('daily_steps_goal', 10000))
        profile.save()
        messages.success(request, 'Settings saved! ⚙️')
        return redirect('accounts:settings')
    return render(request, 'accounts/settings.html', {'profile': profile})
