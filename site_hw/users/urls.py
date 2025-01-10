from django.urls import path
from .views import RegisterView, LoginView, WelcomeView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
