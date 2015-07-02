from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse

from .models import Simulation, Submission, Result
from .forms import SubmitForm

import difflib

# Create your views here.
def index(request):

    # render the template with the error
    def render_error(msg_error):
        return render(request, 'challenge/index.html',
                      {'l_simu': l_simu,
                       'form': form,
                       'error_message': msg_error})

    l_simu = Simulation.objects.all()

    if request.method == 'POST':
        form = SubmitForm(request.POST,l_simu = l_simu)

        if form.is_valid():
            try:
                selected_simu = Simulation.objects.get(name=request.POST['select_simu'])
            except (KeyError, Simulation.DoesNotExist):
                render_error("Wrong selected simulation")

            s = Submission.objects.create(simu=selected_simu,
                                          answer=request.POST['answer'],
                                          user=request.user)

            parsed_answer = s.parse_answer()
            parsed_truth = selected_simu.parse_truth()

            # TODO : Real F1 score

            sm = difflib.SequenceMatcher(None,parsed_answer,parsed_truth)

            r = Result.objects.create(submission=s,f1score=sm.ratio())

            return render(request, 'challenge/index.html',
                          {'l_simu' : l_simu,
                           'form': form,
                           'res': r.f1score})
        else:
            render_error("Invalid Form")

    else:
        form = SubmitForm(l_simu = l_simu)
    
    context = {'l_simu': l_simu, 'form': form}
    return render(request, 'challenge/index.html', context)

    
