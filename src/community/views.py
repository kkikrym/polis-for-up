from django.shortcuts import render
from django.utils.timezone import make_aware
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import Community, CommunityChat, COM_CATEGORIES
from .forms import CommunityCreateForm
from accounts.models import CustomUser
from django.http import HttpResponseRedirect
import datetime
# Create your views here.

class CommunityListView(TemplateView): #/community
    template_name = 'community/index.html'

    def get_context_data(self , **kwargs):
        c = super().get_context_data(**kwargs)
        today = make_aware(datetime.datetime.now())
        start_date = today - datetime.timedelta(days=7)
        cl = sorted(list(Community.objects.prefetch_related('communitychat_set').all()), key=lambda x: len(x.communitychat_set.filter(created_at__range=(start_date, today))) ,reverse=True)
        if self.request.user.is_authenticated:
            c["CommunityCreateForm"] = CommunityCreateForm
            c["joining_community"] = self.request.user.community_set.all()[:3]
            c['community_list'] = cl[:6]
        return c

class JoiningListView(TemplateView):
    template_name = 'community/joining.html'

    def get_context_data(self , **kwargs):
        c = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            c["CommunityCreateForm"] = CommunityCreateForm
            c["joining_community"] = self.request.user.community_set.all()
        return c

class CommunityExploreView(TemplateView):
    template_name = 'community/explore.html'
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        cl = Community.objects.all()
        tab = self.request.GET.get('tab')
        if tab !='0':
            if tab == '4':
                cl = cl.filter(category = 0)
            else:
                cl = cl.filter(category = int(tab))
        order = self.request.GET.get('order')
        if order == '1': # 活況
            cl = list(cl)
            pass
        elif order == '2': # チャット数
            cl = list(cl)
            cl = sorted(cl, key=lambda x: len(x.communitychat_set.all()), reverse=True)
        elif order == '3': # ユーザー数
            cl = list(cl)
            cl = sorted(cl, key=lambda x: len(x.users.all()), reverse=True)
        else: # 新規
            cl = cl.order_by('-created_at')
        c["community_list"] = cl
        return c

class CommunityDetailView(DetailView): #/community/chat/<room_id>
    model = Community
    template_name = 'community/community.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if not self.request.user in self.object.users.all():
                self.object.users.add(self.request.user)

        room_id = self.kwargs['pk']
        chats = CommunityChat.objects.filter(community=room_id)
        context["room_id"] = room_id
        context["category"] = COM_CATEGORIES[int(self.object.category)][1]
        context["community_chats"] = chats
        return context

def join_community(request, pk):
    c = Community.objects.get(id = pk)
    if not request.user in c.users.all():
        c.users.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def exit_community(request, pk):
    c = Community.objects.get(id = pk)
    if request.user in c.users.all():
        c.users.remove(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

class CommunityCreateView(CreateView):
    model = Community
    template_name = 'community/create.html'
    success_url = reverse_lazy('community:index')
    fields = ['community_name', 'description', 'category',]

class CommunityDeleteView(DeleteView):
    model = Community
    template_name = 'community/delete.html'
    success_url = reverse_lazy('community:index')