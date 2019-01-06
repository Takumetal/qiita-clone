from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import FormView, UpdateView
from django.utils.translation import gettext_lazy as _

from accounts.models import UserProfile
from comments.models import Comment
from users.models import User
from posts.models import Post

from .forms import SignUpForm


User_model = get_user_model()


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = '/login/'

    def form_valid(self, form):
        user = form.save()
        user.save()
        messages.success(self.request, _('Sign up is completed.'))
        return redirect('login')


class UserDetailView(DetailView):
    template_name = 'accounts/detail.html'

    queryset = User.objects.all()

    def get_object(self):
        username = self.kwargs.get('username')
        obj = get_object_or_404(User, username=username)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        context['posts'] = Post.objects.filter(create_user=kwargs['object']).order_by('-create_date')
        username = self.kwargs.get('username')
        target_user = get_object_or_404(User, username=username)
        login_user = get_object_or_404(User, username=self.request.user.username)
        context['is_login_user'] = True if target_user.email == login_user.email else False
        context['good_article'] = Post.objects.get_good_article_for_specific_user(self.request.user)
        context['comments'] = Comment.objects.get_comments_for_specific_user(self.request.user)

        return context


class UserEditView(UpdateView):
    template_name = 'accounts/edit.html'
    model = User
    fields = ['username']

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        target_user = get_object_or_404(User, username=username)
        login_user = get_object_or_404(User, username=self.request.user.username)

        if target_user.email != login_user.email:
            return redirect('accounts:detail', username=username)
        else:
            return super().get(request, **kwargs)


class StockListView(ListView):
    template_name = 'accounts/stock.html'

    def get_queryset(self, *args, **kwargs):
        qs = UserProfile.objects.get(user=self.request.user)
        stock_list = []
        if qs.stock:
            for stock in qs.stock.all():
                if stock.tag:
                    stock.tag_list = stock.tag.split(' ')
                stock_list.append(stock)
        return stock_list

    def get_context_data(self, *args, **kwargs):
        context = super(StockListView, self).get_context_data(*args, **kwargs)
        context['stock_list'] = self.get_queryset()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, **kwargs)

    def post(self, request, *args, **kwargs):
        post_pk = request.POST['post_pk']
        post = Post.objects.get(pk=post_pk)
        stock_result = UserProfile.objects.stock_toggle(request.user, post)

        return JsonResponse({'is_stock': stock_result})


class UserFollowView(View):

    def post(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        target_user = User.objects.get(username=username)
        user_follow_result = UserProfile.objects.user_follow_toggle(request.user, target_user)

        return JsonResponse({'is_follow': user_follow_result})
