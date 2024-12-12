from django.http import HttpResponse
from django.shortcuts import render

from .models import User

def hello_world(request):
    return HttpResponse("Привіт, світ!")


def user_list(request):
    users = User.objects.all()
    return render(request, 'hello_app/user_list.html', {'users': users})
