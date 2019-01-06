from django.db import models

from tags.models import Tag
from django.conf import settings
from django.urls import reverse_lazy

from users.models import User


class PostManager(models.Manager):

    def is_good(self, user, post_obj):
        return True if user in post_obj.good.all() else False

    def get_good_count(self, user, post_obj):
        return post_obj.good.all().count()

    def get_good_article_for_specific_user(self, user):
        return Post.objects.filter(good=user)

    def good_toggle(self, user, post_obj):
        if user in post_obj.good.all():
            is_good = False
            post_obj.good.remove(user)
        else:
            is_good = True
            post_obj.good.add(user)
        return is_good

    def post_ranking(self):
        return Post.objects.all().annotate(
            good_counts=models.Count('good')).order_by('-good_counts')[:10]


class Post(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    text = models.TextField(max_length=5000, null=False, blank=False)
    tag = models.CharField(max_length=100, blank=True, null=True)
    good = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, default=None, related_name='good')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='create_user')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('posts:detail', kwargs={'username': self.create_user.username, 'pk': self.pk})
