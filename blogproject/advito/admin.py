from django.contrib import admin
from .models import Profile, Post, CategoryPost, FavoritePost, Comment, Review, Message

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(CategoryPost)
admin.site.register(FavoritePost)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Message)
