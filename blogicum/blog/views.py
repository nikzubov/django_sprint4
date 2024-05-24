from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.db.models.functions import Now
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.edit import FormMixin

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post

userModel = get_user_model()
PAGINATION = 10


class PostPermissionMixin:
    def get_object(self):
        return get_object_or_404(
            Post.objects,
            id=self.kwargs.get(self.post_id_url_kwarg)
        )

    def test_func(self):
        username = Post.objects.filter(
            id=self.kwargs.get(self.post_id_url_kwarg)
        ).values('author__username').first()
        try:
            return self.request.user.username == username.get(
                'author__username'
            )
        except AttributeError:
            raise Http404()


class CommentPermissionMixin:
    def get_object(self):
        return get_object_or_404(
            Comment,
            id=self.kwargs.get(self.comment_id_url_kwarg)
        )

    def test_func(self):
        username = Comment.objects.filter(
            id=self.kwargs['comment_id']
        ).values('author__username').first()
        try:
            return self.request.user.username == username.get(
                'author__username'
            )
        except AttributeError:
            raise Http404()

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class Index(ListView):
    template_name = 'blog/index.html'
    model = Post
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = Post.objects.filter(
            pub_date__lte=Now(),
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')
        query_set = queryset.annotate(
            comment_count=Count('comment')
        )

        return query_set


class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    success_url = reverse_lazy('blog:index')
    form_class = CommentForm
    post_id_url_kwarg = 'post_id'

    def get_object(self):
        post = get_object_or_404(
            Post.objects,
            id=self.kwargs.get(self.post_id_url_kwarg)
        )
        if (post.is_published
            and post.category.is_published
                and post.pub_date <= timezone.now()):
            return post
        elif self.request.user.id == post.author.id:
            return post
        else:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(
            post=self.kwargs.get(self.post_id_url_kwarg)
        ).order_by('created_at')
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostEdit(PostPermissionMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
    template_name = 'blog/create.html'
    post_id_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs.get(
                self.post_id_url_kwarg
            )}
        )

    def handle_no_permission(self):
        return redirect(self.get_success_url())


class PostDelete(PostPermissionMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    post_id_url_kwarg = 'post_id'


class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ('text',)
    template_name = 'blog/comment.html'
    post_id_url_kwarg = 'post_id'

    def get_object(self):
        return get_object_or_404(
            Post.objects,
            id=self.kwargs.get('post_id')
        )

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.post = get_object_or_404(
            Post, id=self.kwargs.get(self.post_id_url_kwarg)
        )
        instance.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs.get(self.post_id_url_kwarg)}
        )


class EditComment(CommentPermissionMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ('text',)
    template_name = 'blog/comment.html'
    comment_id_url_kwarg = 'comment_id'


class DeleteComment(CommentPermissionMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    comment_id_url_kwarg = 'comment_id'


class CategoryView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = PAGINATION

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return context

    def get_queryset(self):
        return Post.objects.filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True,
            pub_date__lte=Now(),
        )


class Profile(ListView):
    model = Post
    paginate_by = PAGINATION
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            userModel,
            username=self.kwargs['username']
        )
        return context

    def get_queryset(self):
        queryset = Post.objects.filter(
            author__username=self.kwargs['username']
        ).order_by('-pub_date')
        query_set = queryset.annotate(comment_count=Count('comment'))

        return query_set


class EditProfile(UserPassesTestMixin, UpdateView):
    model = userModel
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
    )
    template_name = 'blog/user.html'
    username_url_kwarg = 'username'

    def get_object(self):
        return get_object_or_404(
            userModel,
            username=self.kwargs.get(self.username_url_kwarg)
        )

    def get_queryset(self):
        return get_object_or_404(
            userModel,
            username=self.kwargs.get(self.username_url_kwarg)
        )

    def test_func(self):
        try:
            return self.request.user.username == self.kwargs.get(
                self.username_url_kwarg
            )
        except AttributeError:
            raise Http404()

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.kwargs.get(self.username_url_kwarg)}
        )
