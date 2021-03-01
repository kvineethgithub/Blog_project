from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)
    no_of_dislikes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Like(models.Model):
    post_id = models.CharField(max_length=55, null=True)
    user = models.CharField(max_length=55, null=True)

    def __unicode__(self):
        return self.post_id


class Dislike(models.Model):
    post_id = models.CharField(max_length=55, null=True)
    user = models.CharField(max_length=55, null=True)

    def __unicode__(self):
        return self.post_id


class Comment(models.Model):
    post_id = models.CharField(max_length=55, null=True)
    user = models.CharField(max_length=55, null=True)
    comment = models.CharField(max_length=255)

    def __unicode__(self):
        return self.post_id
