from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DetailView, CreateView,
    UpdateView, ListView, DeleteView
)
from django.views.generic.edit import FormMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Comment
from .forms import CommentForm
from django.db.models.functions import Now
from django.db.models import Count


USER_MODEL = get_user_model()


class Index(ListView):
    template_name = 'blog/index.html'
    model = Post
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(
            pub_date__lte=Now(),
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')
        query_set = queryset.annotate(comment_count=Count('comment'))

        return query_set


class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    success_url = reverse_lazy('blog:index')
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(
            post=self.kwargs['pk']
        ).order_by('created_at')
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
    template_name = 'blog/create.html'

    def form_valid(self, form, **kwargs):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostEdit(UpdateView):
    model = Post
    fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class PostDelete(DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ('text',)
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form, **kwargs):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.post = get_object_or_404(Post, id=self.kwargs['pk'])
        instance.save()

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class EditComment(UpdateView):
    model = Comment
    fields = ('text',)
    template_name = 'blog/comment.html'

    def get_success_url(self, **kwargs):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['post_pk']}
        )


class DeleteComment(DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_success_url(self, **kwargs):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['post_pk']}
        )


class CategoryView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

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
    paginate_by = 10
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            USER_MODEL,
            username=self.kwargs['username']
        )
        return context

    def get_queryset(self):
        queryset = Post.objects.filter(
            author__username=self.kwargs['username']
        ).order_by('-pub_date')
        query_set = queryset.annotate(comment_count=Count('comment'))

        return query_set


class EditProfile(UpdateView):
    model = USER_MODEL
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog')

    def get_queryset(self):
        return get_object_or_404(
            USER_MODEL,
            username=self.kwargs['username']
        )
