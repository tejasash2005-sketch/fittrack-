# ⚡ FitTrack — Smart Personal Fitness Tracker

A comprehensive, production-grade Django fitness tracking web application with a premium dark UI.

---

## 🚀 Quick Setup (5 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations accounts workouts diet metrics admin_panel
python manage.py migrate
```

### 3. Seed Sample Data
```bash
python manage.py seed_data
```
This creates:
- 35+ exercises in the library
- 45+ verified food items
- Admin user (admin / admin1234)
- Demo user with 30 days of real data (demo / demo1234)

### 4. Start Server
```bash
python manage.py runserver
```

### 5. Open Browser
```
http://127.0.0.1:8000
```

---

## 🔑 Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin1234` |
| Demo User | `demo` | `demo1234` |

---

## ✨ 25+ Advanced Features

### 💪 Workout Tracking
1. **Workout Session Logger** — Log sessions with name, date, duration, calories, notes
2. **Effort & Mood Tracking** — Rate RPE (1-10) and mood before/after each workout
3. **Workout Streak System** — Daily streak counter with best streak tracking
4. **Exercise Library** — 35+ categorized exercises with difficulty, muscles, calories/min
5. **Workout Plans** — Create multi-week training programs with day-by-day schedules
6. **Personal Records (PRs)** — Track lifetime bests per exercise
7. **Workout Calendar** — Visual monthly calendar showing workout days
8. **Quick Templates** — One-click fill for Push Day, Pull Day, HIIT, Yoga etc.
9. **Heart Rate Logging** — Average and max HR per session

### 🥗 Nutrition & Diet
10. **Daily Meal Logger** — Log meals by type: Breakfast, Lunch, Dinner, Snack, Pre/Post Workout
11. **Macro Dashboard** — Real-time protein/carbs/fat/fiber totals vs goals
12. **Food Database** — 45+ verified foods with full nutritional data
13. **Live Food Search** — Instant AJAX search across food database
14. **Water Intake Tracker** — Log in ml with quick buttons (+200ml, +250ml, etc.)
15. **Nutrition Goals** — Set personalized daily calorie and macro targets
16. **Meal Plans** — Create structured weekly meal programs
17. **Calorie Net Tracking** — See calories consumed vs burned

### 📊 Health Metrics
18. **Body Measurements** — Log weight, body fat %, muscle mass, waist/chest/hips/arms/thighs
19. **BMI Calculator** — Auto-calculated with category (Underweight/Normal/Overweight/Obese)
20. **TDEE Calculator** — Personalized Total Daily Energy Expenditure
21. **Sleep Tracker** — Log duration, quality, interruptions with trend charts
22. **Mood Tracker** — Daily mood (1-5), energy levels, stress rating
23. **Step Counter** — Daily step logging with distance and calories
24. **Progress Photos** — Upload and view visual transformation timeline
25. **Health Goals** — Set and track goals for weight, steps, sleep, water, workouts

### 📈 Analytics & Insights
26. **30-Day Analytics Dashboard** — Weight, calories, steps, and sleep trend charts
27. **Weekly Activity Charts** — Bar + line combo chart on main dashboard
28. **Macro Pie Chart** — Visual daily macro breakdown
29. **Admin Analytics** — User growth, workout activity, system-wide stats

### 👑 Admin Panel
30. **Admin Dashboard** — KPIs, charts, recent users & activity
31. **User Management** — Search, view profiles, grant/revoke premium
32. **Food Database Management** — Add, verify food items
33. **System Statistics** — Full platform metrics

### 🔒 Account Features
34. **User Registration & Login** — Secure auth with profile setup
35. **Profile Customization** — Avatar, bio, fitness goals, activity level
36. **Notifications System** — Achievement, goal, and system notifications
37. **Settings Panel** — Daily goal customization, preferences
38. **Password Change** — Secure password management
39. **Achievement Badges** — Earn badges for milestones (streaks, workouts, goals)

---

## 🏗️ Project Structure

```
fittrack/
├── fittrack/           # Django project settings & URLs
├── accounts/           # User auth, profiles, achievements, notifications
├── dashboard/          # Main dashboard & analytics views
├── workouts/           # Workout sessions, exercises, plans, PRs, streaks
├── diet/               # Meals, food database, water, nutrition goals
├── metrics/            # Body metrics, sleep, mood, steps, health goals
├── admin_panel/        # Admin-only dashboard and management tools
├── templates/          # All HTML templates
│   ├── base.html       # Master layout with sidebar navigation
│   ├── accounts/       # Login, register, profile, settings
│   ├── dashboard/      # Home dashboard, analytics
│   ├── workouts/       # Workout list, log, detail, exercises, calendar
│   ├── diet/           # Nutrition dashboard, meal logging
│   ├── metrics/        # Body metrics, sleep, mood, steps
│   └── admin_panel/    # Admin dashboard, user management
├── static/             # CSS, JS, images
├── media/              # Uploaded files (avatars, progress photos)
├── requirements.txt    # Python dependencies
└── manage.py
```

---

## 🎨 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 |
| Frontend | Bootstrap 5 + Custom CSS |
| Charts | Chart.js 4 |
| Icons | Bootstrap Icons |
| Fonts | Rajdhani + DM Sans + JetBrains Mono |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Media | Pillow |

---

## 🔧 Production Notes

- Change `SECRET_KEY` in `settings.py`
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Use PostgreSQL for production database
- Set up static file serving with WhiteNoise or Nginx
- Configure media file storage (S3 recommended)

---

Built with ❤️ — FitTrack 2024
