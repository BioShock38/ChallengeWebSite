from django.conf.urls import url

from . import views

urlpatterns =  [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<challenge_id>[0-9]+)/$', views.challenge_submit, name='challenge_submit'),
    url(r'^(?P<challenge_id>[0-9]+)/desc/$', views.desc, name='desc'),
    url(r'^(?P<challenge_id>[0-9]+)/rules/$', views.rules, name='rules'),
    url(r'^(?P<challenge_id>[0-9]+)/evaluation/$', views.evaluation, name='evaluation')
]
