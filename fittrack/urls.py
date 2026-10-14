from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import landing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing'),
   
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('workouts/', include('workouts.urls')),
    path('diet/', include('diet.urls')),
    path('metrics/', include('metrics.urls')),
    path('admin-panel/', include('admin_panel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
