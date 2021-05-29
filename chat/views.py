
from django.http import HttpResponse
from django.shortcuts import render

from chat.models import ConnectedUsers


def index(request):
    return render(request, 'index.html')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })


def users_online(request):
    connected_users = [str(user) for user in ConnectedUsers.objects.all()]
    return HttpResponse("Currently connected: %s" % connected_users)
