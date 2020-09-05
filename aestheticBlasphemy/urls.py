"""aestheticBlasphemy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, handler400
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings
from django.conf.urls.static import static

from blogging.sitemaps import BlogSitemap, BlogParentSitemap
from django.contrib.flatpages import views

from functools import partialmethod

from dashboard.views import custom_login
from django.contrib.auth.views import LogoutView

from django.contrib.sitemaps.views import sitemap

app_name="core"

sitemaps =  {'blog':BlogSitemap,
             'sections':BlogParentSitemap,
            }

admin.autodiscover()

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('blog/', include("blogging.urls", namespace="blogging"), name='blogging'),
    path('dashboard/', include('dashboard.urls',namespace='dashboard'), name='dashboard'),
    path('comments/', include('comments.urls', namespace='comments'), name='comments'),
    path('rest/', include("rest.urls", namespace="rest")),
    path('messages/', include("pl_messages.urls", namespace="messages")),
    path('accounts/login/', custom_login),
    path('accounts/logout/', LogoutView.as_view(),{'next_page': '/'}),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps':sitemaps}),
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('', include("blogging.urls", namespace="blogging")),
)
# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)