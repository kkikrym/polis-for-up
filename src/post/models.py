from django.db import models
from accounts.models import CustomUser
import uuid
from team.models import CATEGORIES
from stock.models import Stock
from django.utils import timezone
# Create your models here.
class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    title = models.CharField(max_length=255)

    category = models.CharField(max_length=255, choices=CATEGORIES)

    stock = models.ManyToManyField(Stock, blank=True)

    thumbnail = models.ImageField(blank=True, null=True)

    content = models.TextField()

    is_published = models.BooleanField(default=False)

    seen =models.IntegerField(default=0)

    good =models.IntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)

    updated_at = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(
        CustomUser,
        on_delete = models.DO_NOTHING
    )


    def __str__(self):
        return self.title

class PostGood(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)

    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(default=timezone.now)