from django.contrib import admin
from .models import Profile, Post, CategoryPost, HistoryPost, FavoritePost, Comment

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(CategoryPost)
admin.site.register(HistoryPost)
admin.site.register(FavoritePost)
admin.site.register(Comment)
