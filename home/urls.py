from django.conf.urls import url

import home.views as hv

urlpatterns =  [
    url(r'^$', hv.home, name = 'home')
]
