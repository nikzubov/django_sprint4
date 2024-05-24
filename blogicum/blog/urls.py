from django.urls import path

from . import views

app_name = 'blog'


urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='index'
    ),
    path(
        'profile/<slug:username>/',
        views.Profile.as_view(),
        name='profile'
    ),
    path(
        'profile/<slug:username>/edit_profile/',
        views.EditProfile.as_view(),
        name='edit_profile'
    ),
    path(
        'posts/<int:post_id>/',
        views.PostDetail.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.PostEdit.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.PostDelete.as_view(),
        name='delete_post'
    ),
    path(
        'add_comment/<int:post_id>/',
        views.AddComment.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.EditComment.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.DeleteComment.as_view(),
        name='delete_comment'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryView.as_view(),
        name='category_posts'
    ),
    path(
        'posts/create/',
        views.PostCreate.as_view(),
        name='create_post'
    ),
]
