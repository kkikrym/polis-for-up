from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'mypage'

urlpatterns = [
    path('', views.MypageView.as_view(), name='index'),
    path('change/<uuid:pk>', views.UserChangeView.as_view(), name='change'),
    path('stock_search/', views.StockSearchView.as_view(), name='stock_search'),
    path('followers/', views.FollowersView.as_view(), name='followers'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
