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
        'profile/edit_profile/',
        views.EditProfile.as_view(),
        name='edit_profile'
    ),
    path(
        'posts/<int:pk>/',
        views.PostDetail.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:pk>/edit/',
        views.PostEdit.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:pk>/delete/',
        views.PostDelete.as_view(),
        name='delete_post'
    ),
    path(
        'add_comment/<int:pk>/',
        views.AddComment.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:post_pk>/edit_comment/<int:pk>/',
        views.EditComment.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<int:post_pk>/delete_comment/<int:pk>/',
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
