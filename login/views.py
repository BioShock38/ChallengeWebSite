from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
 
from login.models import Challenger
from django.contrib.auth.models import User
from login.forms import RegistrationForm

import datetime, random, sha
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail



@csrf_protect
def register(request, template_name):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            # create new user
            
            new_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            
            new_user.is_active = False
            new_user.save()

            # Build the activation key for their account

            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+new_user.username).hexdigest()
            
            # Create and save their profile
            new_profile = Challenger(user=new_user,
                                     activation_key=activation_key)
            new_profile.save()
            
            # Send an email with the confirmation link
            email_subject = 'Your new account confirmation'
            email_body = "Hello, %s, and thanks for signing up for an ssmpg 2015 account!\n\nTo activate your account, click this link: \n\nhttp://localhost:8000/login/confirm/%s" % ( new_user.username, new_profile.activation_key )
            send_mail(email_subject,
                      email_body,
                      'kevin.caye@gmail.com',
                      [new_user.email])
            

            return render_to_response(
                'login/success.html',
                RequestContext( request, { 'confirm': True } )
            )
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    template_name,
    variables,
    )
 
    

def confirm(request, activation_key):
    if request.user.is_authenticated():
        return render_to_response('login/confirm.html', RequestContext( request, {'has_account': True}))
    user_profile = get_object_or_404(Challenger,
                                     activation_key=activation_key)
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    return render_to_response('login/confirm.html', RequestContext( request, {'success': True}) )


def register_success(request):
    return render_to_response(
    'login/success.html', request
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home(request):
    return render_to_response(
    'login/home.html',
    RequestContext( request, { 'user': request.user } )
    )
