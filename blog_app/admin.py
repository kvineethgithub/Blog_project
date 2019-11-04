from django.contrib import admin
from .models import Post, Like, Dislike, Comment

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Comment)
