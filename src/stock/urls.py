from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'stock'

urlpatterns = [
    #path('index/', views.IndexView.as_view(), name='index'),
    #path('add_wl/', views.add_wl, name='add_wl'),
    #path('trade/', views.trade, name='trade'),
    #path('search/', views.StockSearchView.as_view(), name='search'),
    #path('delete_trade/<uuid:pk>/', views.delete_trade, name='delete_trade'),
    #path('add_to_post/', views.add_to_post, name='add_to_post'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
