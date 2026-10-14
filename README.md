# fittrack-
# 🏋️ FitTrack — Fitness & Workout Management System

**FitTrack** is a Django-based fitness management web application designed to help users organize workouts, monitor personal fitness progress, manage nutrition, and build consistent fitness habits through a centralized dashboard.

The application combines workout tracking, dietary management, health metrics, and user account management in one platform.

## ✨ Features

### 🏋️ Workout Management
- Track workout sessions and exercise activities.
- Explore available exercises and workout plans.
- View workout history and personal records.
- Organize workouts using a calendar.
- Log and manage individual workout sessions.

### 🥗 Diet & Nutrition
- Maintain daily meal records.
- Browse a food database.
- Create and manage meal plans.
- Set personal nutrition goals.
- Monitor dietary habits.

### 📊 Fitness Metrics & Progress
- Record body measurements and fitness metrics.
- Track daily steps and sleep.
- Log mood and personal wellness information.
- Upload progress photos.
- Set fitness goals and monitor progress.

### 👤 User Account Management
- User registration and login.
- Profile management.
- Account settings and password changes.
- User notifications.

### 🛡️ Administration
- Administrative dashboard.
- User management.
- Exercise and food database management.
- Announcements and achievements management.
- Activity logs and application statistics.
- Premium analytics dashboard.

### 📱 Dashboard & Analytics
- Centralized fitness dashboard.
- Access workout, nutrition, and progress information.
- Review fitness activities and personal records.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django 4.2.7 | Web application framework |
| SQLite | Database |
| HTML5 | Page structure |
| CSS3 | Styling |
| JavaScript | Client-side interactions |
| Pillow | Image processing and progress photo support |
| Django Templates | Dynamic page rendering |

## 📂 Project Structure

```text
FitTrack/
├── accounts/          # User accounts and authentication
├── admin_panel/       # Administrative functionality
├── dashboard/         # Main dashboard
├── diet/              # Diet and nutrition management
├── metrics/           # Fitness metrics and progress
├── workouts/          # Workout and exercise management
├── fittrack/          # Django project configuration
├── templates/         # HTML templates
├── media/             # Uploaded media and progress photos
├── db.sqlite3         # Local development database
├── manage.py          # Django management utility
├── requirements.txt   # Python dependencies
├── run.bat            # Windows startup script
└── README.md
```

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or a compatible Python version
- pip
- Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/FitTrack.git
cd FitTrack
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

### 7. Open the application

Visit the following address in your browser:

```text
http://127.0.0.1:8000/
```

## 🔐 Administration

To create a Django administrator account, run:

```bash
python manage.py createsuperuser
```

Follow the prompts to create your administrator credentials.

If the Django admin interface is enabled, it is generally accessible at:

```text
http://127.0.0.1:8000/admin/
```

## 🎯 Project Objectives

- Simplify workout and exercise tracking.
- Provide a centralized platform for fitness management.
- Support nutrition planning and daily habit tracking.
- Help users record personal progress over time.
- Demonstrate full-stack web development using Django and relational databases.

## 🚀 Future Enhancements

- Interactive fitness analytics and progress charts.
- Personalized workout recommendations.
- Integration with wearable fitness devices.
- AI-assisted workout and nutrition recommendations.
- Mobile-responsive enhancements and deployment to a production environment.

## 👨‍💻 About the Project

FitTrack is a fitness management web application built with Python and Django. It demonstrates practical implementation of backend development, database operations, authentication, modular application architecture, and dynamic web interfaces.

## 📄 License

Add a license file if you intend to distribute this project under an open-source license.

