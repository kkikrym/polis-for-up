from django.views.generic import TemplateView
from account.forms import CustomLoginForm, CustomSignupForm
# Create your views here.


class TopView(TemplateView):
    template_name = 'top/index.html'
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c["CustomLoginForm"] = CustomLoginForm
        return c

class AboutView(TemplateView):
    template_name = 'top/about.html'