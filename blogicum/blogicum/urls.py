from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy
from django.conf.urls.static import static
from django.conf import settings

handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.server_error'

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog'),
        ),
        name='registration',
    ),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)