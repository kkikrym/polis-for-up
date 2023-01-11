from django.contrib import admin
from .models import Post
# Register your models here.
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(Post, PostAdmin)