from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    #path('', views.UserIndexView.as_view(), name='index'),
    path('detail/<uuid:pk>', views.UserDetailView.as_view(), name='detail'),



]

from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)