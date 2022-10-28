from django.contrib import admin

from .models import (
    Post,
    Followers,

)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'header', 'text_post', 'read_or_not']
    list_editable = ['header', 'text_post']


@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'following_user_id', 'created']


