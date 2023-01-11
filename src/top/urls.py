from django.urls import include, path
from . import views

app_name = 'top'

urlpatterns = [
    path('', views.TopView.as_view(), name='index'),
    path('about', views.AboutView.as_view(), name='about')
]
