from django.conf.urls import url

import home.views as hv

urlpatterns =  [
    url(r'^home/$', hv.home, name = 'home'),
    url(r'^help/$', hv.helpPage, name = 'help'),
]
