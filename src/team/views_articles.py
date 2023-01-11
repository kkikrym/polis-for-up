class TeamArticleCreateView(CreateView):
    model = TeamArticle
    template_name = 'team/article_create.html'
    form_class = TeamArticleCreateForm

    def get_success_url(self):
        return reverse_lazy('team:top', kwargs={'pk':self.kwargs["team_id"]})

    def form_valid(self, form):
        a = form.save(commit=False)
        a.team = Team.objects.get(id = self.kwargs["team_id"])
        a.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_id'] = self.kwargs["team_id"]
        return context

class TeamArticleDetailView(DetailView):
    model = TeamArticle
    template_name = 'team/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = CATEGORY_DIC
        return context