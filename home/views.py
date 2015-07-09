from login.views import register
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    return register( request, 'home/home.html' )


def helpPage(request):
    return render_to_response(
    'home/help.html', RequestContext( request, { 'user': request.user } )
    )
