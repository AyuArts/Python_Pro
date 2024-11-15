from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Імпортуємо settings
from django.conf.urls.static import static
from accounts import views as accounts_views

urlpatterns = [
    path('', accounts_views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
