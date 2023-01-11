from django.db import models
import uuid
from accounts.models import CustomUser
from django.utils import timezone
# Create your models here.

CURRENCY_CHOICES = [
    ('JPY', 'JPY'),
    ('USD', 'USD'),
]

class Stock(models.Model):
    stock_id = models.CharField(
        max_length = 255,
        unique = True,
    )

    json = models.JSONField(default=dict, blank=True, null=True)

    watch_user = models.ManyToManyField(CustomUser, default=None, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stock_id

class Trade(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False )

    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)

    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    price = models.FloatField()

    amount = models.IntegerField()

    currency = models.CharField(max_length=255, choices=CURRENCY_CHOICES)

    trade_date = models.DateTimeField()

    sell = models.BooleanField()

    created_at = models.DateTimeField(default=timezone.now)
