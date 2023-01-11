from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.edit import CreateView ,UpdateView, DeleteView
from accounts.models import CustomUser
from stock.forms import StockSearchForm
from .forms import TeamCreateForm, UserChangeForm
from post.models import Post, PostGood
from stock.models import Stock
from team.models import Team, TeamRecruit, TeamArticle
from django.db.models import Prefetch
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from django.utils.timezone import make_aware
import datetime
yf.pdr_override()
import json

def recent_rate(*args):
    now = datetime.date.today()
    yst = now - datetime.timedelta(days=5)
    tom = now + datetime.timedelta(days = 1)
    l = []
    for ticker in args:
        a = {}
        df = pdr.get_data_yahoo(ticker, start=yst, end=tom)
        cs = df.loc[:, "Close"].tolist()
        d = cs[-1] - cs[-2]
        t = d/cs[0]*100
        a["ticker"] = ticker
        a["fluc"] = t
        l.append(a)
    return l


# CustomUser変更 UpdateView
class UserChangeView(UpdateView):
    template_name = 'mypage/change.html'
    model = CustomUser
    fields = [
        'username',
        'handle_name',
        'profile_message',
        'profile_image',
    ]

    def get_success_url(self):
        return reverse_lazy('mypage:index')


class MypageView(TemplateView):
    template_name = 'mypage/index.html'

    def get(self,*args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('account_login')
        else:
            return super().get(self,*args, **kwargs)

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        p = Post.objects.prefetch_related('postgood_set').all()
        ta = TeamArticle.objects.prefetch_related('tagood_set').all()
        #1日のいいねの数でソート
        al = list(p.filter(is_published=True)) + list(ta.filter(is_published=True))
        today = make_aware(datetime.datetime.now())
        start_date = today - datetime.timedelta(days=1)
        al = sorted(al, key=lambda x: len(x.postgood_set.filter(created_at__range=(start_date, today))) if x in p else len(x.tagood_set.filter(created_at__range=(start_date, today))), reverse=True)
        goods = sum([ len(x.postgood_set.all()) for x in list(p.filter(is_published=True).filter(author = self.request.user))])
        #おすすめチーム
        t = Team.objects.prefetch_related('teamarticle_set').all()[0:11]
        t = [ x for x in t if len(x.users.all())<=7]
        t = sorted(t, key=lambda x: sum([ len(y.tagood_set.all()) for y in x.teamarticle_set.all() ]), reverse=True)
        t_goods = [ sum([ len(x.tagood_set.all()) for x in list(ta.filter(is_published=True).filter(team = y))]) for y in t ]

        c["team_recommends"] = t
        c["recommend_goods"] = t_goods
        c["post_list"] = p.filter(author_id= CustomUser.objects.get(user_id=self.request.user.pk)).order_by('-created_at')
        try:
            c["post_today"] = al[0]
        except:
            pass
        c["rising_posts"] = al[1:11]
        c["p_fst"] = c["post_list"].first()
        c["recruits"] = TeamRecruit.objects.prefetch_related('team').filter(user=self.request.user)
        c["TeamCreateForm"] = TeamCreateForm
        c["UserChangeForm"] = UserChangeForm(instance=self.request.user)
        c["goods"] = goods
        return c

class StockSearchView(FormView):
    form_class = StockSearchForm
    template_name = 'post/search.html'
    success_url = reverse_lazy('mypage:stock_search')
    posted_data = {'stock_id': ""}

    def form_valid(self, form):
        self.posted_data['stock_id'] = form.data.get('stock_id')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.date.today()
        context["data_list"] = []
        stk = self.posted_data['stock_id']
        try:
            ticker_info = yf.Ticker(stk)
            df = ticker_info.history(period='max')
            date = [d.strftime('%Y-%m-%d') for d in df.index]
            close = df.loc[:, 'Close'].tolist()
            a = []
            context["stock_id"] = stk
            for n in range(len(df)):
                b = {}
                b["date"] = date[n]
                b["close"] = close[n]
                a.append(b)
            context["data_list"] = a
            self.request.session["data_list"] = context["data_list"]
            self.request.session["stock_id"] = stk
        except:
            a = [{"date":now, "close":0}]
            context["data_list"] = a
            context["er"] = "sorry, there was no stock data you indicated"
        return context

class FollowersView(TemplateView):
    template_name = 'mypage/followers.html'

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c["following_teams"] = Team.objects.filter(followers = self.request.user)
        return c
