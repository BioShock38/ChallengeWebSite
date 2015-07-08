from django.conf.urls import url

import login.views as lv

urlpatterns =  [
   url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login/login.html'}, name = 'signin'),
    url(r'^home/$', lv.home),
    url(r'^logout/$', lv.logout_page, name = 'signout'),
    url(r'^register/$', lv.register, name = 'signup'),
    url(r'^register/success/$', lv.register_success),
]
