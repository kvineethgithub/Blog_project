from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^register/', user_register, name='register'),
    url(r'^logout/', user_logout, name='logout'),
    url(r'^user_profile/', user_profile, name='user_profile'),
    url(r'^home/', home_page, name='home'),
    url(r'^uploaded_blogs/', uploaded_blogs, name='uploaded_blogs'),
    url(r'^blog_create/', blog_create, name='blog_create'),
    url(r'^detail_blog_view/(?P<id>\d+)/', detail_blog_view, name='detail_blog_view'),
    url(r'^delete_blog/(?P<id>\d+)/', delete_blog, name='delete_blog'),
    url(r'^edit_blog/(?P<id>\d+)/', edit_blog, name='edit_blog'),
    url(r'^likes_view/(?P<id>\d+)/', likes_view, name='likes_view'),
    url(r'^dislikes_view/(?P<id>\d+)/', dislikes_view, name='dislikes_view'),
    url(r'^liked_users/(?P<id>\d+)/', liked_users, name='liked_users'),
    url(r'^disliked_users/(?P<id>\d+)/', disliked_users, name='disliked_users'),
    url(r'^comments_view/(?P<id>\d+)/', comments_view, name='comments_view'),
]
