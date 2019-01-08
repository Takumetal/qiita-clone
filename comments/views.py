from django.contrib import messages
from django.http.response import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.views.generic import View

from posts.models import Post

from .models import Comment


class CommentView(View):
#     http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        pk = self.kwargs.get('pk')
        commented_username = request.user.username
        text = request.POST.get('text', None)
        result = Comment.objects.create_comment(commented_username, pk, text)

        if request:
            messages.success(request, _('Posted a comment.'))
        else:
            messages.error(request, _('Failed to post a comment.'))

        return redirect('posts:detail', username=username, pk=pk)


class CommentGoodView(View):

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk', None)
        comment_obj = Comment.objects.get(pk=pk)
        result = Post.objects.good_toggle(request.user, comment_obj)

        return JsonResponse({'is_good': result, 'good_comment_count': Comment.objects.get_good_count(request.user, comment_obj)})
