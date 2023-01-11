import uuid
from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
# Create your models here.

COM_CATEGORIES = [
    ("0", "その他"),
    ("1", "投資関連"),
    ("2", "リクルート"),
    ("3", "雑談"),
]


class Community(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False )

    users = models.ManyToManyField(CustomUser)

    community_name = models.CharField(max_length=255)

    description = models.TextField()

    leader = models.CharField(max_length=255)

    category = models.CharField(max_length=255, choices=COM_CATEGORIES)

    created_at = models.DateTimeField(
        default=timezone.now
    )

class CommunityChat(models.Model):
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING)

    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    whats_in = models.CharField(max_length=255, default=None)

    user_image = models.CharField(max_length=255, default=None, null=True,blank=True)

    good = models.IntegerField(default=0)

    content = models.TextField(default=None)

    created_at = models.DateTimeField(default=timezone.now)