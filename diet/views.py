from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import date, timedelta
from .models import MealEntry, FoodItem, WaterIntake, MealPlan, NutritionGoal
import json


@login_required
def diet_dashboard(request):
    today = date.today()
    selected_date = request.GET.get('date', str(today))
    try:
        selected_date = date.fromisoformat(selected_date)
    except:
        selected_date = today

    meals = MealEntry.objects.filter(user=request.user, date=selected_date).select_related('food_item')
    water_logs = WaterIntake.objects.filter(user=request.user, date=selected_date)
    goal, _ = NutritionGoal.objects.get_or_create(user=request.user)

    totals = {
        'calories': sum(m.total_calories for m in meals),
        'protein': sum(m.total_protein for m in meals),
        'carbs': sum(m.total_carbs for m in meals),
        'fat': sum(m.total_fat for m in meals),
    }
    total_water = sum(w.amount_ml for w in water_logs)

    meals_by_type = {}
    for meal in meals:
        mt = meal.meal_type
        if mt not in meals_by_type:
            meals_by_type[mt] = []
        meals_by_type[mt].append(meal)

    # Weekly nutrition chart
    week_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        day_meals = MealEntry.objects.filter(user=request.user, date=d)
        week_data.append({
            'day': d.strftime('%a'),
            'calories': float(sum(m.total_calories for m in day_meals)),
            'protein': float(sum(m.total_protein for m in day_meals)),
        })

    context = {
        'selected_date': selected_date,
        'today': today,
        'meals': meals,
        'meals_by_type': meals_by_type,
        'water_logs': water_logs,
        'total_water_ml': total_water,
        'total_water_l': round(total_water / 1000, 2),
        'totals': totals,
        'goal': goal,
        'week_data': json.dumps(week_data),
        'calorie_pct': min(round((totals['calories'] / goal.daily_calories) * 100) if goal.daily_calories else 0, 100),
        'protein_pct': min(round((totals['protein'] / goal.daily_protein) * 100) if goal.daily_protein else 0, 100),
        'carbs_pct': min(round((totals['carbs'] / goal.daily_carbs) * 100) if goal.daily_carbs else 0, 100),
        'fat_pct': min(round((totals['fat'] / goal.daily_fat) * 100) if goal.daily_fat else 0, 100),
    }
    return render(request, 'diet/dashboard.html', context)


@login_required
def add_meal(request):
    foods = FoodItem.objects.all()
    if request.method == 'POST':
        food_id = request.POST.get('food_item')
        food = get_object_or_404(FoodItem, pk=food_id)
        MealEntry.objects.create(
            user=request.user,
            food_item=food,
            meal_type=request.POST.get('meal_type', 'lunch'),
            date=request.POST.get('date', date.today()),
            quantity=float(request.POST.get('quantity', 1)),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, f'{food.name} added to your meal log! 🥗')
        return redirect('diet:dashboard')
    return render(request, 'diet/add_meal.html', {'foods': foods, 'today': date.today()})


@login_required
def delete_meal(request, pk):
    meal = get_object_or_404(MealEntry, pk=pk, user=request.user)
    meal.delete()
    messages.success(request, 'Meal entry deleted.')
    return redirect('diet:dashboard')


@login_required
def add_water(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 250))
        WaterIntake.objects.create(user=request.user, date=date.today(), amount_ml=amount)
        return JsonResponse({'success': True, 'amount': amount})
    return JsonResponse({'success': False})


@login_required
def food_search(request):
    q = request.GET.get('q', '')
    foods = FoodItem.objects.filter(name__icontains=q)[:10] if q else []
    data = [{'id': f.id, 'name': f.name, 'calories': f.calories, 'protein': f.protein,
              'carbs': f.carbohydrates, 'fat': f.fat, 'category': f.category} for f in foods]
    return JsonResponse({'foods': data})


@login_required
def food_database(request):
    category = request.GET.get('category', '')
    foods = FoodItem.objects.all()
    if category:
        foods = foods.filter(category=category)
    return render(request, 'diet/food_database.html', {'foods': foods, 'category': category})


@login_required
def meal_plans(request):
    plans = MealPlan.objects.filter(user=request.user)
    return render(request, 'diet/meal_plans.html', {'plans': plans})


@login_required
def nutrition_goals(request):
    goal, _ = NutritionGoal.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        goal.daily_calories = int(request.POST.get('daily_calories', 2000))
        goal.daily_protein = float(request.POST.get('daily_protein', 150))
        goal.daily_carbs = float(request.POST.get('daily_carbs', 200))
        goal.daily_fat = float(request.POST.get('daily_fat', 65))
        goal.daily_fiber = float(request.POST.get('daily_fiber', 25))
        goal.daily_water_ml = int(request.POST.get('daily_water_ml', 2500))
        goal.save()
        messages.success(request, 'Nutrition goals updated! 🎯')
        return redirect('diet:goals')
    return render(request, 'diet/nutrition_goals.html', {'goal': goal})
