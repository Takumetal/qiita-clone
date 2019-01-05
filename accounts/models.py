from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from posts.models import Post
from tags.models import Tag
from users.models import User


class UserProfileManager(models.Manager):

    def stock_toggle(self, user, post):
        if post in user.profile.stock.all():
            is_stock = False
            user.profile.stock.remove(post)
        else:
            is_stock = True
            user.profile.stock.add(post)
        return is_stock

    def is_stock(self, user, post):
        return True if post in user.profile.stock.all() else False

    def tag_follow_toggle(self, user, tag):
        if tag in user.profile.tag.all():
            is_follow = False
            user.profile.tag.remove(tag)
        else:
            is_follow = True
            user.profile.tag.add(tag)
        return is_follow

    def user_follow_toggle(self, user, target_user):
        if target_user in user.profile.following.all():
            is_follow = False
            user.profile.following.remove(target_user)
        else:
            is_follow = True
            user.profile.following.add(target_user)
        return is_follow

    def user_follow_ranking(self):
        users = list(User.objects.all())
        users = sorted(users, key=lambda x: x.followed_by.count(), reverse=True)
        users = users[:10]
        return users


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.DO_NOTHING)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_by')
    stock = models.ManyToManyField(Post, related_name='stock')
    tag = models.ManyToManyField(Tag, related_name='followed_tag')

    objects = UserProfileManager()

    def __str__(self):
        return self.user.username


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)

