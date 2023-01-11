from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'community'

urlpatterns = [
    path('', views.CommunityListView.as_view(), name='index'),
    path('chat/<uuid:pk>/', views.CommunityDetailView.as_view(), name='community'),
    path('create/', views.CommunityCreateView.as_view(), name='create'),
    path('delete/<uuid:pk>', views.CommunityDeleteView.as_view(), name='delete'),
    path('joining/', views.JoiningListView.as_view(), name='joining'),

    path('join/<uuid:pk>/', views.join_community, name='join'),
    path('exit/<uuid:pk>/', views.exit_community, name='exit'),

    path('explore/', views.CommunityExploreView.as_view(), name='explore'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
