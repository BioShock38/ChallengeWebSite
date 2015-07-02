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
import login.views as lv
import home.views as hv

# Only during development see  http://stackoverflow.com/questions/9181047/django-static-files-development and see https://docs.djangoproject.com/en/1.8/howto/static-files/ for deploy
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login/login.html'}, name = 'signin'),
    url(r'^home/$', lv.home),
    url(r'^logout/$', lv.logout_page, name = 'signout'),
    url(r'^register/$', lv.register, name = 'signup'),
    url(r'^register/success/$', lv.register_success),
    url('^$', hv.home, name = 'home'),
] 

urlpatterns += staticfiles_urlpatterns()
