from django.shortcuts import render

def home_view(request):
    """
    Відображає головну сторінку.

    :param request: Об'єкт HTTP-запиту.
    :return: HTTP-відповідь з вмістом головної сторінки.
    """
    return render(request, 'main_home/home.html')

def about_view(request):
    """
    Відображає сторінку 'Про нас'.

    :param request: Об'єкт HTTP-запиту.
    :return: HTTP-відповідь з вмістом сторінки 'Про нас'.
    """
    return render(request, 'main_home/about.html')

def contact_view(request):
    """
    Відображає сторінку контакту.

    :param request: Об'єкт HTTP-запиту.
    :return: HTTP-відповідь з вмістом сторінки контакту.
    """
    return render(request, 'main_home/contact.html')

def post_view(request, post_id):
    """
    Відображає сторінку публікації з певним ідентифікатором.

    :param request: Об'єкт HTTP-запиту.
    :param post_id: Ідентифікатор публікації.
    :return: HTTP-відповідь з вмістом сторінки публікації.
    """
    context = {
        'post_id': post_id
    }
    return render(request, 'main_home/post.html', context)

def profile_view(request, username):
    """
    Відображає сторінку профілю користувача.

    :param request: Об'єкт HTTP-запиту.
    :param username: Ім'я користувача для профілю.
    :return: HTTP-відповідь з вмістом сторінки профілю користувача.
    """
    context = {
        'username': username
    }
    return render(request, 'main_home/profile.html', context)

def event_view(request, year, month, day):
    """
    Відображає сторінку події з конкретною датою.

    :param request: Об'єкт HTTP-запиту.
    :param year: Рік події.
    :param month: Місяць події.
    :param day: День події.
    :return: HTTP-відповідь з вмістом сторінки події.
    """
    context = {
        'year': year,
        'month': month,
        'day': day
    }
    return render(request, 'main_home/event.html', context)
