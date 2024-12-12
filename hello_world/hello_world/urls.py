from django.contrib import admin
from django.urls import path
from hello_app.views import hello_world, user_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hello_world, name='hello_world'),
    path('users/', user_list, name='user_list'),
]