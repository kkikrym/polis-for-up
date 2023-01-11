import uuid
from django.db import models
from accounts.models import CustomUser
from stock.models import Stock
import json
from django.utils import timezone


# Create your models here.

#from django.core.files.base import ContentFile
#from sorl.thumbnail import get_thumbnail, delete

CATEGORIES = [
    ("0", "その他"),
    ("1", "株式分析"),
    ("2", "経済分析"),
    ("3", "運用手法"),
]

CATEGORY_DIC = {
    "0": "その他",
    "1": "株式分析",
    "2": "経済分析",
    "3": "運用手法",
}

class Team(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False )

    team_name = models.CharField(max_length=255)

    users = models.ManyToManyField(CustomUser, default=None, blank=True)

    leader = models.ForeignKey('accounts.CustomUser', on_delete=models.DO_NOTHING, default=None, blank=True, related_name='leader')

    followers = models.ManyToManyField('accounts.CustomUser', default=None, blank=True, related_name='team_follower')

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(
        default=timezone.now
    )

class TeamThread(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    thread_name = models.CharField(max_length=255)

    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(default=timezone.now)

class TeamChat(models.Model):
    thread = models.ForeignKey(TeamThread, on_delete=models.DO_NOTHING)

    user_id = models.CharField(max_length=255, default="guest")

    whats_in = models.CharField(max_length=255, default=None)

    user_image = models.CharField(max_length=255, default=None, null=True,blank=True)

    seen = models.ManyToManyField(CustomUser, default=None, blank=True)

    good = models.IntegerField(default=0)

    content = models.TextField(default=None)

    created_at = models.DateTimeField(default=timezone.now)

class TeamRequest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)

    message = models.TextField(default=None, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

class TeamRecruit(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)

    message = models.TextField(default=None, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)


class TeamArticle(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)

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

class TAGood(models.Model):
    teamarticle = models.ForeignKey(TeamArticle, on_delete=models.DO_NOTHING)

    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(default=timezone.now)

"""
    def save(self, *args, **kwargs):
        super(self).save(*args, **kwargs)
        temp_img_name = self.image.name
        if self.image.width > 500 or self.image.height > 500:
            new_width = 500
            new_height = 500

            resized = get_thumbnail(self.image, "{}x{}".format(new_width, new_height))
            name = resized.name.split('/')[-1] # 結局上で定義したUUIDの名前になるのでこれは仮の名前
            self.image.save(name, ContentFile(resized.read()), True)
            try:
                delete(temp_img_name)
            except NotFound: # ここの例外は自身のものに変える
                pass
"""