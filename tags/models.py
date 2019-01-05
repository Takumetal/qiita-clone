from django.db import models
from enum import unique


class TagManager(models.Manager):

    def tag_ranking(self):
        from posts.models import Post
        tag_ranking = {}
        for tag in Tag.objects.all():
            tag_ranking[tag.tag] = Post.objects.filter(tag__contains=tag.tag).count()
        return sorted(tag_ranking.items(), key=lambda x: x[1], reverse=True)


class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True, null=False, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)

    objects = TagManager()

    def __str__(self):
        return self.tag
