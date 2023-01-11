from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'team'

urlpatterns = [
    # For those who have not joined team
    path('', views.TeamListView.as_view(), name='index'),
    path('create/', views.TeamCreateView.as_view(), name='create'),
    path('detail/<uuid:pk>/', views.TeamDetailView.as_view(), name='detail'),
    path('change/<uuid:pk>/', views.team_change, name='change'),


    # Team functions for members
    path('top/', views.TeamTopView.as_view(), name='top'),
    path('info/<uuid:pk>/', views.TeamInfoView.as_view(), name='info'),
    path('exit_team/<uuid:pk>/', views.exit_team, name='exit_team'),
    # for leader only
    path('delete/<uuid:pk>/', views.TeamDeleteView.as_view(), name='delete'),
    path('member_delete/<uuid:team_id>/<uuid:user_id>/', views.member_delete, name='member_delete'),

    # chat functions
    path('chat/<uuid:room_id>/', views.TeamChatView.as_view(), name='team'),
    path('thread/delete/<uuid:pk>/', views.ThreadDeleteView.as_view(), name="thread_delete"),
    path('thread/create/<uuid:team_id>/', views.ThreadCreateView.as_view(), name='thread_create'),

    # requests
    path('request/create/<uuid:pk>/', views.create_team_request, name='request_create'),
    path('request/accept/<uuid:pk>/', views.accept_team_request, name='request_accept'),
    path('request/reject/<uuid:pk>/', views.reject_team_request, name='request_reject'),
    path('recruit/create/<uuid:pk>/', views.recruit, name='recruit'),
    path('recruit/accept/<uuid:pk>/', views.accept_recruit, name="accept_recruit"),

    # articles
    path('article/create/<uuid:team_id>/', views.TeamArticleCreateView.as_view(), name='article_create'),
    path('article/update/<uuid:pk>/', views.TeamArticleUpdateView.as_view(), name='article_update'),
    path('article/detail/<uuid:pk>/', views.TeamArticleDetailView.as_view(), name='article_detail'),
    path('article/delete/<uuid:pk>/', views.delete_article, name='article_delete'),
    path('article/ta_good/<uuid:pk>/', views.ta_good, name='ta_good'),
    path('article/ta_ungood/<uuid:pk>/', views.ta_ungood, name='ta_ungood'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
