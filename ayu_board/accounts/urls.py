from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Реєстрація нового користувача
    path('register/', views.register_view, name='register'),

    # Перегляд профілю поточного користувача
    path('profile/', views.profile_view, name='profile'),

    # Перегляд профілю користувача за його ім'ям
    path('profile/<str:username>/', views.profile_view, name='profile_view'),

    # Редагування профілю
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),

    # Зміна паролю
    path('change_password/', views.change_password_view, name='change_password'),

    # Видалення облікового запису
    path('delete_account/', views.delete_account_view, name='delete_account'),

    # Сторінка входу
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # Сторінка виходу
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
