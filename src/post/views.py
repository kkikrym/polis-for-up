from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView ,UpdateView, DeleteView
from accounts.models import CustomUser
from post.models import Post, PostGood
from post.forms import PostCreateForm
from stock.views import StockSearchView
from stock.forms import StockSearchForm
import datetime
from django.http import HttpResponseRedirect
from team.models import CATEGORY_DIC
from stock.models import Stock
from stock.views import STOCK_DIC, JAPANESE_TICKERS
import json
# Create your views here.


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'post/create.html'
    model = Post
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.date.today()
        try:
            context["data_list"] = self.request.session["data_list"]
        except:
            pass
        return context

    def form_valid(self, form):
        f = form.save(commit=False)
        uid = self.request.user.pk
        f.author = CustomUser.objects.get(pk=uid)
        if not f.thumbnail:
            l = ["thumb-other.png", "thumb-stock.png", "thumb-econ.png", "thumb-strategy.png"]
            f.thumbnail = l[int(f.category)]
        f.save()
        if self.request.POST.get("tickerinput"):
            try:
                ticker = self.request.POST.get("tickerinput").split(" ")[0]
                if ticker in JAPANESE_TICKERS:
                    ticker = self.request.POST.get("tickerinput").split(" ")[0].split(".T")[0]
                else:
                    ticker = self.request.POST.get("tickerinput").split(" ")[0].lower()
                stk = Stock.objects.filter(stock_id = ticker)
                f.stock.set(stk)
            except:
                import traceback
                traceback.print_exc()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mypage:index')

class PostListView(ListView):
    model = Post
    template_name = 'post/index.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post/detail.html'

    def get_context_data(self , **kwargs):
        c = super().get_context_data(**kwargs)
        c["category"] = CATEGORY_DIC
        p = c["post"]
        p.seen = int(p.seen) + 1
        p.save()
        c["a"] = p
        c["good_users"] = [ good.user for good in p.postgood_set.all() ]
        if p.stock.first():
            c["json"] = p.stock.first().json
        # page before
        if not "/post/detail/" in str(self.request.META.get('HTTP_REFERER')):
            self.request.session["pre_page"] = self.request.META.get('HTTP_REFERER')
        return c

class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'post/create.html'
    model = Post
    form_class = PostCreateForm

    def get(self,*args, **kwargs):
        if self.request.user != self.get_object().author:
            return redirect('account_login')
        else:
            return super().get(self,*args, **kwargs)

    def form_valid(self, form):
        f = form.save(commit=False)
        f.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mypage:index')

def delete_post(request, pk):
    a = Post.objects.get(id = pk)
    if request.user == a.author:
        goods = PostGood.objects.filter(post=a)
        goods.delete()
        a.delete()
    else:
        pass
    return redirect('mypage:index')

def good(request,pk):
    a = Post.objects.get(pk=pk)
    u =request.user
    PostGood.objects.create(post=a, user=u)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ungood(request, pk):
    a = Post.objects.get(pk=pk)
    u =request.user
    pg = PostGood.objects.filter(post=a)
    pg.filter(user=u).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



