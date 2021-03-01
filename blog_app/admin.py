from django.contrib import admin
from .models import Post, Like, Dislike, Comment


class PostAdmin(admin.ModelAdmin):
    list_filter = ("title", 'pub_date', 'author')
    list_display = ("title", 'content', 'author')


admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Comment)
