from django.contrib import admin
from .models import Stock, Trade
# Register your models here.
admin.site.register(Stock)
admin.site.register(Trade)