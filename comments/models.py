from django.db import models
from django.conf import settings
from django.utils import timezone

from posts.models import Post
from users.models import User


class CommentManager(models.Manager):

    def create_comment(self, username, pk, text):
        comment = self.model(
            text=text,
            post=Post.objects.get(pk=pk),
            post_user=User.objects.get(username=username),
            create_date=timezone.now(),
            update_date=timezone.now(),
        )
        comment.save(using=self._db)
        return comment

    def get_comments_for_specific_post(self, user, post):
        comments = Comment.objects.filter(post=post)
        for comment in comments:
            comment.is_good = True if user in comment.good.all() else False
        return comments

    def get_comments_for_specific_user(self, user):
        return Comment.objects.filter(post_user=user).order_by('-create_date')

    def comment_good_toggle(self, user, comment_obj):
        if user in comment_obj.good.all():
            is_good = False
            comment_obj.good.remove(user)
        else:
            is_good = True
            comment_obj.good.add(user)
        return is_good

    def get_good_count(self, user, comment_obj):
        return comment_obj.good.all().count()


class Comment(models.Model):
    text = models.TextField(max_length=2500, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, related_name='comments')
    good = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='good_comment')
    post_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='post_user')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    def __str__(self):
        return str(self.pk)
