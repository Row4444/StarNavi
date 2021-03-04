from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, verbose_name='Title')
    body = models.TextField(verbose_name='Body')
    date_of_create = models.DateTimeField(default=timezone.now)


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_of_like = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('author', 'post')
