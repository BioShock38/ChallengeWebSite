"""challengewebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

# Only during development see  http://stackoverflow.com/questions/9181047/django-static-files-development and see https://docs.djangoproject.com/en/1.8/howto/static-files/ to deploy
from django.conf.urls.static import static
import home.views as hv

urlpatterns = [
    url(r'^challenge/', include('challenge.urls',namespace='challenge')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', include('login.urls',namespace='login')),
    url(r'^account/', include('account.urls',namespace='account')),
    url(r'^$', hv.home, name = 'home'),
    url(r'^home/', include('home.urls',namespace='home')),
    url(r'^captcha/', include('captcha.urls')),
]

# Only during development see  http://stackoverflow.com/questions/9181047/django-static-files-development and see https://docs.djangoproject.com/en/1.8/howto/static-files/ to deploy
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
