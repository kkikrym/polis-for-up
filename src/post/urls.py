from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'post'

urlpatterns = [
    #path('', views.PostListView.as_view(), name='index'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('detail/<uuid:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('update/<uuid:pk>/', views.PostUpdateView.as_view(), name='update'),
    path('delete/<uuid:pk>/', views.delete_post, name='delete'),
    path('detail/<uuid:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('good/<uuid:pk>/',views.good, name='good'),
    path('ungood/<uuid:pk>/', views.ungood, name='ungood'),
]
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)