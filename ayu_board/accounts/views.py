from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, UserProfileForm, PasswordChangeForm
from .models import UserProfile
from django.contrib.auth.models import User

def home_view(request):
    """
    Головна сторінка.

    Якщо користувач автентифікований, перенаправляє на сторінку профілю.
    Інакше відображає домашню сторінку.

    :param request: HTTP-запит
    :type request: HttpRequest
    :return: Відповідь HTTP
    :rtype: HttpResponse
    """
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        return render(request, 'accounts/home.html')

def register_view(request):
    """
    Реєстрація нового користувача.

    При успішній реєстрації створюється новий обліковий запис і профіль користувача.

    :param request: HTTP-запит
    :type request: HttpRequest
    :return: Відповідь HTTP
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Реєстрація успішна!')
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def edit_profile_view(request):
    """
    Редагування профілю користувача.

    :param request: HTTP-запит
    :type request: HttpRequest
    :return: Відповідь HTTP
    :rtype: HttpResponse
    """
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль оновлено успішно!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def change_password_view(request):
    """
    Зміна паролю користувача.

    Після зміни паролю сесія оновлюється, щоб уникнути виходу користувача.

    :param request: HTTP-запит
    :type request: HttpRequest
    :return: Відповідь HTTP
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Пароль змінено успішно!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def profile_view(request, username=None):
    """
    Відображення профілю користувача.

    Якщо передано ім'я користувача, відображається профіль цього користувача.
    Інакше відображається профіль поточного користувача.

    :param request: HTTP-запит
    :type request: HttpRequest
    :param username: Ім'я користувача
    :type username: str, optional
    :return: Відповідь HTTP
    :rtype: HttpResponse
    """
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    return render(request, 'accounts/profile.html', {'user_profile': user.userprofile})

@login_required
def delete_account_view(request):
    """
    Видалення облікового запису користувача.

    Після видалення перенаправляє на домашню сторінку.

    :param request: HTTP-запит
    :type request: HttpRequest
    :return: Відповідь HTTP
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Ваш обліковий запис було видалено.')
        return redirect('home')
    return render(request, 'accounts/delete_account.html')
