from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('ideas/', views.IdeasSearchView.as_view(), name='ideas'),
    path('users/', views.UsersSearchView.as_view(), name='users'),
    path('teams/', views.TeamsSearchView.as_view(), name='teams'),

    # following
    path('follow_team/<uuid:pk>', views.follow_team, name='follow_team'),
    path('unfollow_team/<uuid:pk>', views.unfollow_team, name='unfollow_team'),

    path('follow/<uuid:pk>', views.follow_user, name='follow_user'),
    path('unfollow/<uuid:pk>', views.unfollow_user, name='unfollow_user'),
    #path('timeline/', views.TimelineView.as_view(), name='timeline'),

]