from django.contrib import admin
from .models import TeamChat, Team, TeamThread, TeamRequest,TeamRecruit , TeamArticle
# Register your models here.
admin.site.register(TeamChat)
admin.site.register(Team)
admin.site.register(TeamThread)
admin.site.register(TeamRequest)
admin.site.register(TeamRecruit)
admin.site.register(TeamArticle)