from django.contrib import admin
from .models import Category, Location, Post, Comment


admin.site.empty_value_display = 'Не задано'


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'image',
        'is_published',
    )
    list_editable = ('is_published', 'category', 'pub_date',)
    search_fields = ('title',) 
    list_filter = ('category',)
    list_display_links = ('author',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text')
    search_fields = ('post', 'text',)
    list_filter = ('post',)
    list_editable = ('text',)
    list_display_links = ('author', 'post',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug')
    search_fields = ('slug',)
    list_editable = ('slug',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
