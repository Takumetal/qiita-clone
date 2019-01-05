from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View

from posts.models import Post
from accounts.models import UserProfile

from .models import Tag


class TagListView(ListView):
    template_name = 'tags/tag_list.html'

    def get_queryset(self, *args, **kwargs):
        qs = Tag.objects.all()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(TagListView, self).get_context_data(*args, **kwargs)
        tag_count_list = {}
        tag_list = context['tag_list']
        for tag in tag_list:
            tag_count_list[tag.tag] = Post.objects.filter(tag__contains=tag).count()
        context['tag_count_list'] = sorted(tag_count_list.items(), key=lambda x: x[1], reverse=True)
        return context


class TagDetailView(DetailView):
    template_name = 'tags/tag_detail.html'

    queryset = Post.objects.all()

    def get_object(self):
        tag = self.kwargs.get('tag')
        target_tag_obj = Tag.objects.get(tag=tag)
        obj = Post.objects.filter(tag__contains=target_tag_obj.tag)
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(TagDetailView, self).get_context_data(*args, **kwargs)
        context['post_list'] = self.get_object()
        context['target_tag'] = Tag.objects.get(tag=self.kwargs['tag'])
        return context


class TagFollowView(View):

    def post(self, request, *args, **kwargs):
        tag = self.kwargs.get('tag')
        is_follow = True if request.POST['is_follow'] == 'true' else False
        target_tag = Tag.objects.get(tag=tag)
        tag_follow_result = UserProfile.objects.tag_follow_toggle(request.user, target_tag)

        return JsonResponse({'is_follow': tag_follow_result})
