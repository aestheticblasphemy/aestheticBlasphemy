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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from django.conf import settings

from blogging.sitemaps import BlogSitemap, BlogParentSitemap
from django.conf.urls.static import static
from django.contrib.flatpages import views

urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include('dashboard.urls',namespace='dashboard')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^blog/', include("blogging.urls", namespace="blogging")),
    url(r'^rest/', include("rest.urls", namespace="rest")),
    url(r'^messages/', include("pl_messages.urls", namespace="messages")),
    url(r'^accounts/login/$', 'dashboard.views.custom_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', 
                                        {'sitemaps': {
                                                      'blog':BlogSitemap,
                                                      'sections':BlogParentSitemap
                                                      }}),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^rest/', include('rest.urls', namespace="rest")),
    url(r'^about/', views.flatpage, {'url': '/about/'}, name='about'),
    url(r'^$', include("blogging.urls", namespace="blogging")),
    url(r'^', include("blogging.urls", namespace="blogging")),
)
# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)