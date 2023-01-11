from typing import List
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.edit import CreateView ,UpdateView, DeleteView
from django.db.models import Q
from django.utils.timezone import make_aware
import datetime
from django.http import HttpResponseRedirect
from .forms import SearchForm
from accounts.models import CustomUser
from team.models import Team, TeamArticle
from post.models import Post
from django.utils import timezone
from team.models import CATEGORY_DIC
# Create your views here.

class IndexView(TemplateView):
    template_name = 'search/index.html'

    def get_context_data(self , **kwargs):
        c = super().get_context_data(**kwargs)
        us = CustomUser.objects.all()
        ts = Team.objects.all()
        p = Post.objects.all()
        ta = TeamArticle.objects.all()

        c["idea_list"] = list(p) + list(ta)
        c["customuser_list"] = us
        c["team_list"] = ts
        return c

class IdeasSearchView(TemplateView):
    template_name = 'search/ideas.html'

    def get_context_data(self , **kwargs):
        c = super().get_context_data(**kwargs)
        p = Post.objects.prefetch_related('author').filter(is_published=True)
        ta = TeamArticle.objects.prefetch_related('team').filter(is_published=True)
        if self.request.GET.get('category'):
            category = self.request.GET.get('category')
            p = p.filter(category = category)
            ta = ta.filter(category = category)
        if self.request.GET.get('search'):
            txt = self.request.GET.get('search')
            p = p.filter(title__icontains = txt)
            ta = ta.filter(title__icontains = txt)
        if self.request.GET.get('order'):
            order = self.request.GET.get('order')
            if order == '0':
                al = list(p) + list(ta)
                al = sorted(al, key=lambda x: x.created_at, reverse=True)
            elif order == '1':
                al = list(p) + list(ta)
                today = make_aware(datetime.datetime.now())
                start_date = today - datetime.timedelta(days=1)
                #1日のいいねの数でソート
                al = sorted(al, key=lambda x: len(x.postgood_set.filter(created_at__range=(start_date, today))) if x in p else len(x.tagood_set.filter(created_at__range=(start_date, today))), reverse=True)
            elif order == '2':
                al = list(p) + list(ta)
                al = sorted(al, key=lambda x: x.seen, reverse=True)
            elif order == '3':
                al = list(p) + list(ta)
                al = sorted(al, key=lambda x: len(x.postgood_set.all()) if x in p else len(x.tagood_set.all()), reverse=True) #いいねの数でソート
        else:
            al = list(p) + list(ta)
            al = sorted(al, key=lambda x: x.created_at, reverse=True)
        c["idea_list"] = al
        return c

class UsersSearchView(TemplateView):
    template_name = 'search/users.html'

    def get_context_data(self , **kwargs):
        c = super().get_context_data(**kwargs)
        cu = CustomUser.objects.prefetch_related('post_set').all()
        if self.request.GET.get('category'):
            if self.request.GET.get('category')=='1':
                cu = cu.filter(team_id = None)
        if self.request.GET.get('search'):
            txt = self.request.GET.get('search')
            cu = cu.filter(username__icontains = txt)
        today = make_aware(datetime.datetime.now())
        start_date = today - datetime.timedelta(days=7)
        if self.request.GET.get('order'):
            order = self.request.GET.get('order')
            if order == '0':
                #1週間のいいねの数でソート
                cu = sorted(cu, key=lambda x: sum([ len(y.postgood_set.all()) for y in x.post_set.all() ]), reverse=True)
            elif order == '1':
                cu = sorted(cu, key=lambda x: x.date_joined, reverse=True)
            elif order == '2':
                cu = sorted(cu, key=lambda x: sum([ len(y.postgood_set.all()) for y in x.post_set.all() ]), reverse=True)
            elif order == '3':
                cu = sorted(cu, key=lambda x: len(x.followed_by.all()), reverse=True)
        else:
            #1週間のいいねの数でソート
            cu = sorted(cu, key=lambda x: sum([ len(y.postgood_set.all()) for y in x.post_set.all() ]), reverse=True)
        c["customuser_list"] = cu
        return c

class TeamsSearchView(TemplateView):
    template_name = 'search/teams.html'

    def get_context_data(self , **kwargs):
        c = super().get_context_data(**kwargs)
        t = Team.objects.prefetch_related('teamarticle_set').all()
        if self.request.GET.get('search'):
            txt = self.request.GET.get('search')
            t = t.filter(team_name__icontains = txt)
        today = make_aware(datetime.datetime.now())
        start_date = today - datetime.timedelta(days=7)
        if self.request.GET.get('order'):
            order = self.request.GET.get('order')
            if order == '0':
                #1週間のいいねの数でソート
                t = [ x for x in t if len(x.users.all())<=7]
                t = sorted(t, key=lambda x: sum([ len(y.tagood_set.all()) for y in x.teamarticle_set.all() ]), reverse=True)
            elif order == '1':
                t = sorted(t, key=lambda x: sum([ len(y.tagood_set.all()) for y in x.teamarticle_set.all() ]), reverse=True)
            elif order == '2':
                t = sorted(t, key=lambda x: len(x.followers.all()), reverse=True)
        else:
            t = [ x for x in t if len(x.users.all())<=7]
            t = sorted(t, key=lambda x: sum([ len(y.tagood_set.all()) for y in x.teamarticle_set.all() ]), reverse=True)
        c["team_list"] = t
        return c

class TimelineView(TemplateView):
    template_name = 'search/timeline.html'

    def get_context_data(self , **kwargs):
        c = super().get_context_data(**kwargs)
        u = self.request.user
        if self.request.user.is_authenticated:
            fu = u.following.all()
            ft = Team.objects.filter(followers=u)
            pl = Post.objects.prefetch_related('author').filter(is_published=True).filter(author__in = fu )
            tal = TeamArticle.objects.prefetch_related('team').filter(is_published=True).filter(team__in = ft)

            al = list(tal) + list(pl)
            al = sorted(al, key= lambda x: x.created_at, reverse = True)
            c["a_list"] = al
            c["category"] = CATEGORY_DIC
        return c


"""
regarding followings
"""


def follow_user(request, pk):
    u = CustomUser.objects.get(pk = pk)
    request.user.following.add(u)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unfollow_user(request, pk):
    u = CustomUser.objects.get(pk = pk)
    request.user.following.remove(u)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def follow_team(request, pk):
    t = Team.objects.get(pk = pk)
    t.followers.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unfollow_team(request, pk):
    t = Team.objects.get(pk = pk)
    t.followers.remove(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))