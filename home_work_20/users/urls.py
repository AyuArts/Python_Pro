from django.urls import path, include

from .views import (
    CustomLoginView,
    RegisterView,
    CustomPasswordResetView,
    ProfileView
)

urlpatterns = [
    # Встроенные маршруты аутентификации
    path('auth/', include('django.contrib.auth.urls')),

    # Кастомные маршруты
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
]
