from django.views.generic import ListView, DetailView
from accounts.models import CustomUser
from team.models import TeamRecruit
from post.models import Post
from django.http import HttpResponseRedirect
# Create your views here.
class UserIndexView(ListView):
    model = CustomUser
    template_name = 'users/index.html'

class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'users/detail.html'
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        u = c["customuser"]
        p = Post.objects.prefetch_related('postgood_set').filter(is_published = True).filter(author = u)
        goods = sum([ len(x.postgood_set.all()) for x in list(p)])
        c["goods"] = goods
        c["top_articles"] = sorted(list(p), key=lambda x:len(x.postgood_set.all()), reverse=True)[:4]
        c["post_list"] = p
        c["recruits"] = TeamRecruit.objects.prefetch_related('team').filter(user = c["customuser"])
        c["recruit_teams"] = [ r.team for r in c["recruits"] ]
        return c