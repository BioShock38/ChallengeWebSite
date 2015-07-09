from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from .models import Challenge, Simulation, Submission, Result
from .forms import SubmitForm

import difflib

# Create your views here.
def index(request):
    l_challenges = Challenge.objects.all()
    context = {'lchallenges': l_challenges}
    return render(request, 'challenge/index.html', context)

def desc(request,challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    context = {'challenge': challenge}
    return render(request, 'challenge/desc.html', context)

def rules(request,challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    context = {'challenge': challenge}
    return render(request, 'challenge/rules.html', context)

def evaluation(request,challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    context = {'challenge': challenge}
    return render(request, 'challenge/evaluation.html', context)

def leaderboard(request,challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    if request.user.is_authenticated():
        context = {'challenge': challenge,"userid": request.user.id}
    else:
        context = {'challenge': challenge}
    return render(request, 'challenge/leaderboard.html', context)

def results_challenge(request,challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    l_results = Result.objects.filter(submission__challenge=challenge) \
                              .filter(submission__simu__private=False) \
                              .values('f1score','submission__date',
                                      'submission__user__username',
                                      'submission__user__id',
                                      'submission__simu',
                                      'submission__simu__name',
                                      'submission__methods')
    return JsonResponse(list(l_results),safe=False)


def challenge_submit(request,challenge_id):

    # render the template with the error
    def render_error(msg_error):
        return render(request, 'challenge/submit.html',
                      {'l_simu': l_simu,
                       'form': form,
                       'challenge': challenge,
                       'error_message': msg_error})

    challenge = Challenge.objects.get(id=challenge_id)
    l_simu = Simulation.objects.filter(challenge__id=challenge_id)

    if request.method == 'POST':
        form = SubmitForm(request.POST,l_simu = l_simu)

        if not request.user.is_authenticated():
            render_error("You must be logged in.")

        if form.is_valid():
            try:
                selected_simu = Simulation.objects.get(name=request.POST['select_simu'])
            except (KeyError, Simulation.DoesNotExist):
                render_error("Wrong selected simulation")

            (soft,option) = (request.POST['software_0'],request.POST['software_1'])
            if int(soft) < len(Submission.SOFTWARE_CHOICES)-1:
                software = Submission.SOFTWARE_CHOICES[int(soft)][1]
            else:
                software = option

            s = Submission.objects.create(simu=selected_simu,
                                          challenge=challenge,
                                          answer=request.POST['answer'],
                                          date=timezone.now(),
                                          methods=software,
                                          user=request.user)

            parsed_answer = s.parse_answer()
            parsed_truth = selected_simu.parse_truth()

            # TODO : Real F1 score

            sm = difflib.SequenceMatcher(None,parsed_answer,parsed_truth)

            r = Result.objects.create(submission=s,f1score=sm.ratio())

            if selected_simu.private:
                return render(request, 'challenge/submit.html',
                          {'l_simu' : l_simu,
                           'form': form,
                           'challenge': challenge,
                           'res': "Submitted !"
                          })
            else :
            	return render(request, 'challenge/submit.html',
                          {'l_simu' : l_simu,
                           'form': form,
                           'challenge': challenge,
                           'res': str(r.f1score)})
        else:
            render_error("Invalid Form")

    else:
        form = SubmitForm(l_simu = l_simu)

    context = {'l_simu': l_simu, 'form': form, 'challenge':challenge}
    return render(request, 'challenge/submit.html', context)


