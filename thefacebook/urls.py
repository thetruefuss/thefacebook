"""thefacebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin

from accounts import views as accounts_views
from core import views as core_views

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^contact/$', core_views.contact, name='contact'),
    url(r'^terms/$', core_views.terms, name='terms'),
    url(r'^privacy/$', core_views.privacy, name='privacy'),
    url(r'^about/$', core_views.about, name='about'),
    url(r'^faq/$', core_views.faq, name='faq'),

    url(r'^login/$', accounts_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^profile/$', accounts_views.profile, name='profile'),
    url(r'^search/$', accounts_views.search, name='search'),
    url(r'^settings/edit_info/$', accounts_views.edit_info, name='edit_info'),
    url(r'^settings/edit_picture/$', accounts_views.edit_picture, name='edit_picture'),

    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
