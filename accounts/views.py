from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
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


class UserListView(ListView):
    template_name = 'accounts/user_list.html'

    def get_queryset(self, *args, **kwargs):
        qs = User.objects.all().order_by('username')
        paginator = Paginator(qs, settings.USER_LIST_PER_PAGE)

        page_num = self.request.GET.get('page', 1)
        user_list = paginator.get_page(page_num)
        return user_list

    def get_context_data(self, *args, **kwargs):
        context = super(UserListView, self).get_context_data(*args, **kwargs)
        context['user_list'] = self.get_queryset()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, **kwargs)


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
        tag_count_dict = {}
        if qs.stock:
            for stock in qs.stock.all():
                if stock.tag:
                    stock.tag_list = stock.tag.split(' ')
                    for tag in stock.tag_list:
                        if tag not in tag_count_dict.keys():
                            tag_count_dict[tag] = 1
                        else:
                            tag_count_dict[tag] += 1
                stock_list.append(stock)
        return stock_list, tag_count_dict

    def get_context_data(self, *args, **kwargs):
        context = super(StockListView, self).get_context_data(*args, **kwargs)
        stock_list, tag_count_dict = self.get_queryset()
        context['stock_list'] = stock_list
        context['tag_count_dict'] = dict(sorted(tag_count_dict.items(), key=lambda x: x[1], reverse=True))
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
