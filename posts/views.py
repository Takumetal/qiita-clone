from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from accounts.models import UserProfile
from users.models import User
from tags.models import Tag
from comments.models import Comment

from .forms import CreatePostModelForm, UpdatePostModelForm
from .models import Post


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'posts/index.html'

    def get_queryset(self, *args, **kwargs):
        qs = Post.objects.all().order_by('-create_date')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['user_follow_ranking'] = UserProfile.objects.user_follow_ranking()
        context['tag_ranking'] = Tag.objects.tag_ranking()
        context['post_ranking'] = Post.objects.post_ranking()
        return context


class DetailView(DetailView):
    template_name = 'posts/detail.html'

    queryset = Post.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Post, pk=pk)
        if obj.tag:
            obj.tag = obj.tag.split(' ')
        obj.is_good = Post.objects.is_good(self.request.user, obj)
        obj.good_count = Post.objects.get_good_count(self.request.user, obj)
        obj.is_stock = UserProfile.objects.is_stock(self.request.user, obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['object'] = post
        username = self.kwargs.get('username')
        target_user = get_object_or_404(User, username=username)
        login_user = get_object_or_404(User, username=self.request.user.username)
        context['is_login_user'] = True if target_user.email == login_user.email else False
        context['comments'] = Comment.objects.get_comments_for_specific_post(self.request.user, post)

        return context


class PostCreateView(CreateView):
    template_name = 'posts/create.html'
    form_class = CreatePostModelForm
    model = Post

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.create_user = User.objects.get(email=request.user.email)
            form_obj.save()
            messages.success(request, _('You posted an article!'))
            return redirect('posts:index')

        return render(request, self.template_name, {'form': form})


class PostUpdateView(UpdateView):
    template_name = 'posts/update.html'
    form_class = UpdatePostModelForm
    model = Post

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        target_post = Post.objects.get(pk=pk)
        target_user = get_object_or_404(User, username=target_post.create_user.username)
        login_user = get_object_or_404(User, username=self.request.user.username)

        if target_user.email != login_user.email:
            return redirect('posts:detail', username=target_user.username, pk=self.kwargs['pk'])
        else:
            return super().get(request, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.success(request, _("{title} Updated post!".format(title=self.object.title)))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostDeleteView(DeleteView):
    model = Post

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, _('{title} Deleted.').format(title=self.object.title))
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy( 'accounts:detail', kwargs={'username': username})


class PostGoodView(View):

    def post(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        pk = self.kwargs.get('pk')
        is_good = True if request.POST['is_good'] == 'true' else False
        target_post = Post.objects.get(pk=pk)
        good_result = Post.objects.good_toggle(request.user, target_post)

        return JsonResponse({'is_good': good_result, 'good_count': Post.objects.get_good_count(request.user, target_post)})