from django.utils.timezone import make_aware
import datetime
from pipes import Template
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView, TemplateView
from django.urls import reverse_lazy
from .models import CATEGORY_DIC, Team, TeamChat, TeamThread, TeamRequest, TeamRecruit, TeamArticle, TAGood
from accounts.models import CustomUser
from django.http import HttpResponseRedirect
from .forms import TeamArticleCreateForm, ChatMessageForm, ThreadCreateForm, TeamChangeForm
from stock.models import Stock
from stock.views import STOCK_DIC, JAPANESE_TICKERS
# Create your views here.


def get_team_requests_for_user(func):
    def wrapper(self,  *args, **kwargs):
        c = func(self)
        if self.request.user.is_authenticated:
            c["teamrequest_list"] = [t.team for t in self.request.user.teamrequest_set.all()]
        return c
    return wrapper

"""
Regarding the team function
"""

class TeamCreateView(CreateView):
    model = Team
    template_name = 'team/create.html'
    fields = ['team_name']

    def form_valid(self, form):
        team = form.save(commit=False)
        uid = self.request.user.user_id
        u = CustomUser.objects.get(user_id=uid)
        team.leader = u
        team.save()
        u.team_id = team.id
        u.save()
        team.users.add(u)
        return redirect("mypage:index")

class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'team/delete.html'
    success_url = reverse_lazy('team:index')

    def form_valid(self, form):
        u = CustomUser.objects.get(user_id=self.request.user.user_id)
        u.team_id = ""
        u.save()
        return super().form_valid(form)

class TeamListView(ListView):
    model = Team
    template_name = 'team/index.html'

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        t = Team.objects.prefetch_related('teamarticle_set').all()
        if self.request.GET.get('search'):
            txt = self.request.GET.get('search')
            t = t.filter(team_name__icontains = txt)
        if self.request.GET.get('order'):
            order = self.request.GET.get('order')
            if order == '0':
                today = make_aware(datetime.datetime.now())
                start_date = today - datetime.timedelta(days=7)
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
        t = [ x for x in t if len(x.users.all()) <= 9 ]
        c["team_list"] = t
        return c

class TeamDetailView(DetailView):
    model = Team
    template_name = 'team/detail.html'

    def get_context_data(self , **kwargs):
        c = super().get_context_data(**kwargs)
        t = c["team"]
        tas = TeamArticle.objects.prefetch_related('tagood_set').filter(is_published=True).filter(team=t.pk)
        c["top_articles"] = sorted(list(tas), key=lambda x:len(x.tagood_set.all()), reverse=True)[:4]
        c["teamarticles"] = tas.order_by('-created_at')
        c["goods"] = sum([len(x.tagood_set.all()) for x in tas])
        if self.request.user.is_authenticated:
            c["user_requests"] = [ x.team for x in self.request.user.teamrequest_set.prefetch_related("team").all() ]
        return c

def team_change(request, pk):
    t = Team.objects.get(pk = pk)
    n = request.POST.get('team_name')
    d = request.POST.get('description')
    t.team_name = n
    t.description = d
    t.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





"""
View for team top for team members
"""



class TeamTopView(TemplateView):
    template_name = 'team/top.html'

    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.user.team_id
        team = Team.objects.get(pk=pk)
        ta = TeamArticle.objects.prefetch_related('tagood_set').filter(is_published=True)
        #1日のいいねの数でソート
        al = list(ta)
        today = make_aware(datetime.datetime.now())
        start_date = today - datetime.timedelta(days=1)
        al = sorted(al, key=lambda x: len(x.tagood_set.filter(created_at__range=(start_date, today))), reverse=True)
        context["team_id"] = pk
        context["team"] = Team.objects.get(pk = pk)
        context["thread_list"] = TeamThread.objects.filter(team=pk)
        context["r_list"] = TeamRequest.objects.prefetch_related('user').filter(team=team)
        context["rising_posts"] = al[0:10]
        context["thread_create_form"] = ThreadCreateForm
        context["article_list"] = TeamArticle.objects.prefetch_related('team').filter(team=team).order_by('-created_at')
        context["TeamChangeForm"] = TeamChangeForm(instance=Team.objects.get(pk=pk))
        return context

class TeamInfoView(DetailView):
    model = Team
    template_name = 'team/info.html'

    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context["thread_list"] = TeamThread.objects.filter(team=pk)
        context["team_id"] = pk
        return context

def team_create(request):
    u = request.user
    team = Team(leader = u.user_id)
    team.save()
    u.team_id = team.id
    u.save()
    team.users.add(u)
    return reverse_lazy('mypage:index', request.user.user_id)


"""
Regarding the threads function
"""


class TeamChatView(DetailView):
    model = Team
    template_name = 'team/chat.html'

    def get(self, request, room_id):
        context = {}
        chats = list(TeamChat.objects.filter(thread=room_id).values())
        for i,item in enumerate(chats):
            user = CustomUser.objects.get(user_id=item['user_id'])
            chats[i]['username'] = user.username
            chats[i]['user_image'] = user.profile_image
        t = TeamThread.objects.get(id=room_id)
        context["room_id"] = room_id
        context['thread'] = t
        context["thread_chats"] = chats

        context["team"] = t.team
        context["team_id"] = t.team.id
        context["thread_list"] = TeamThread.objects.filter(team=t.team)
        context["thread_create_form"] = ThreadCreateForm
        return render(request, 'team/chat.html', context)

class ThreadCreateView(CreateView):
    model = TeamThread
    template_name = 'team/thread_create.html'
    fields = ['thread_name']

    def get_success_url(self):
        return reverse_lazy('team:top')

    def form_valid(self, form):
        thread = form.save(commit=False)
        thread.team = Team.objects.get(id=self.kwargs["team_id"])
        thread.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tid = self.kwargs["team_id"]
        context["team_id"] = tid
        context["thread_list"] = TeamThread.objects.filter(team=tid)

        return context

class ThreadDeleteView(DeleteView):
    model = TeamThread
    template_name = 'team/delete.html'

    def get_success_url(self):
        return reverse_lazy('team:top')



"""
Regarding members
"""

def member_delete(request, team_id, user_id):
    t = Team.objects.get(id=team_id)
    t.users.remove(CustomUser.objects.get(pk=user_id))
    u = CustomUser.objects.get(pk=user_id)
    u.team_id = None
    u.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def exit_team(request, pk):
    t = Team.objects.get(pk = pk)
    if request.user in t.users.all():
        if request.user == t.leader:
            if len(t.users.all()) == 1:
                t.users.remove(request.user)
                request.user.team_id = None
                request.user.save()
                t.save()
            else:
                t.leader = CustomUser.objects.get(pk = request.GET.get('pre_leader'))
                t.users.remove(request.user)
                request.user.team_id = None
                request.user.save()
                t.save()
        else:
            t.users.remove(request.user)
            request.user.team_id = None
            request.user.save()
            t.save()
    return redirect('search:teams')

def create_team_request(request, pk):
    uid = request.user.user_id
    TeamRequest.objects.create(team = Team.objects.get(id=pk),user=request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def confirm_team_request(request):
    return

def accept_team_request(request, pk):
    r = TeamRequest.objects.get(id=pk)
    t = r.team
    t.users.add(r.user)
    t.save()
    u = r.user
    u.team_id = t.id
    u.save()
    r.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def reject_team_request(request,pk):
    r = TeamRequest.objects.get(id=pk)
    r.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def recruit(request,pk):
    u = CustomUser.objects.get(pk = pk)
    t = request.user.team_set.first()
    if request.user == t.leader:
        if not t in [ r.team for r in u.teamrecruit_set.all() ]:
            TeamRecruit.objects.create(user=u, team=t)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def accept_recruit(request, pk):
    u = request.user
    r = TeamRecruit.objects.get(pk=pk)
    t = r.team
    if not u.team_set.first():
        if len(t.users.all()) <= 9:
            t.users.add(u)
            t.save()
            u.team_id = t.id
            u.save()
            r.delete()
    return redirect('team:top')

"""
Regarding team articles
"""

class TeamArticleCreateView(CreateView):
    model = TeamArticle
    template_name = 'team/article_create.html'
    form_class = TeamArticleCreateForm

    def get_success_url(self):
        return reverse_lazy('team:top')

    def form_valid(self, form):
        a = form.save(commit=False)
        t = Team.objects.get(id = self.kwargs["team_id"])
        if self.request.user in t.users.all():
            a.team = t
            if not a.thumbnail:
                l = ["thumb-other.png", "thumb-stock.png", "thumb-econ.png", "thumb-strategy.png"]
                a.thumbnail = l[int(a.category)]
            a.save()
            if self.request.POST.get("tickerinput"):
                try:
                    ticker = self.request.POST.get("tickerinput").split(" ")[0]
                    if ticker in JAPANESE_TICKERS:
                        ticker = self.request.POST.get("tickerinput").split(" ")[0].split(".T")[0]
                    else:
                        ticker = self.request.POST.get("tickerinput").split(" ")[0].lower()
                    stk = Stock.objects.filter(stock_id = ticker)
                    a.stock.set(stk)
                except:
                    import traceback
                    traceback.print_exc()
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_id'] = self.kwargs["team_id"]
        return context

class TeamArticleUpdateView(UpdateView):
    model = TeamArticle
    template_name = 'team/article_create.html'
    form_class = TeamArticleCreateForm

    def get(self, request, *args, **kwargs):
        if not request.user in self.get_object().team.users.all():
            return redirect('account_login')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('team:top')

    def form_valid(self, form):
        a = form.save(commit=False)
        if not a.thumbnail:
            l = ["thumb-other.png", "thumb-stock.png", "thumb-econ.png", "thumb-strategy.png"]
            a.thumbnail = l[int(a.category)]
        a.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team_id"] = self.object.team.id
        return context


class TeamArticleDetailView(DetailView):
    model = TeamArticle
    template_name = 'team/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = CATEGORY_DIC
        ta = context["teamarticle"]
        ta.seen += 1
        ta.save()
        context["a"] = ta
        if ta.stock.first():
            context["json"] = ta.stock.first().json
        context["good_users"] = [ good.user for good in ta.tagood_set.prefetch_related('user').all() ]
        if not '/team/article/detail/' in str(self.request.META['HTTP_REFERER']):
            self.request.session["pre_page"] = self.request.META['HTTP_REFERER']
        return context

def delete_article(request, pk):
    a = TeamArticle.objects.get(id = pk)
    tpk = a.team.pk
    if request.user == a.team.leader:
        goods = TAGood.objects.filter(teamarticle = a)
        goods.delete()
        a.delete()
    else:
        pass
    return redirect('team:top')

def ta_good(request,pk):
    a = TeamArticle.objects.get(id = pk)
    u = request.user
    TAGood.objects.create(teamarticle = a, user = u)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ta_ungood(request,pk):
    a = TeamArticle.objects.get(id = pk)
    u = request.user
    ta = TAGood.objects.filter(teamarticle = a)
    ta.filter(user=u).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




