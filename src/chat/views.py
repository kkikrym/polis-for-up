from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from accounts.models import CustomUser
# Create your views here.
def index(request):
    return render(request, 'chat/index.html', {})

class TeamView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'chat/index.html'



def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })