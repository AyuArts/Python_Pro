from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    # Відображає головну сторінку сайту.

    path('about/', views.about_view, name='about'),
    # Відображає сторінку "Про нас".

    path('contact/', views.contact_view, name='contact'),
    # Відображає сторінку з контактною інформацією.

    re_path(r'^post/(?P<post_id>\d+)/$', views.post_view, name='post'),
    # Відображає сторінку публікації за ідентифікатором.
    # :param id: Ідентифікатор публікації, має бути числом.

    re_path(r'^profile/(?P<username>\w[a-zA-Z]+)/$', views.profile_view, name='profile'),
    # Відображає сторінку профілю користувача.
    # :param username: Ім'я користувача, складається з літер.

    re_path(r'^event/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.event_view, name='event'),
    # Відображає сторінку події за датою.
    # :param year: Рік події (4 цифри).
    # :param month: Місяць події (2 цифри).
    # :param day: День події (2 цифри).
]
