from django.shortcuts import render
import socket
from photo.models import Album


# Create your views here.


def home_view(request):
    context = {
        'title': 'Ana Sayfa',
        'hostname': socket.gethostname(),
    }

    return render(request, 'home/home.html', context)
