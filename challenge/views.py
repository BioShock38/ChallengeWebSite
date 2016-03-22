from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.utils.html import escape
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import csv

from .models import Challenge, Dataset, Submission, Result
from .forms import SubmitForm


# Create your views here.
@login_required(login_url='/login/login/')
def index(request):
    l_challenges = Challenge.objects.all()
    context = {'lchallenges': l_challenges}
    return render(request, 'challenge/index.html', context)

@login_required(login_url='/login/login/')
def desc(request,challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    context = {'challenge': challenge}
    return render(request, 'challenge/desc.html', context)

@login_required(login_url='/login/login/')
def rules(request,challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    context = {'challenge': challenge}
    return render(request, 'challenge/rules.html', context)

@login_required(login_url='/login/login/')
def evaluation(request,challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    context = {'challenge': challenge}
    return render(request, 'challenge/evaluation.html', context)

@login_required(login_url='/login/login/')
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
                                      'submission__simu__private',
                                      'submission__user__username',
                                      'submission__user__id',
                                      'submission__simu',
                                      'submission__simu__name',
                                      'submission__methods')
    for res in l_results:
        for key, value in res.iteritems():
            if type(value) == unicode:
                res[key] = escape(value)
                
    return JsonResponse(list(l_results),safe=False)

def csv_generate(request,challenge_id):
    response = HttpResponse(content_type='text/csv')
    content_disposition = 'attachment; filename="csv_challenge{challengeid}.csv"'
    content_disposition_formated = content_disposition.format(challengeid=challenge_id)
    response['Content-Disposition'] = content_disposition_formated

    writer = csv.writer(response, delimiter='\t')

    challenge = Challenge.objects.get(id=challenge_id)
    results = Result.objects.filter(submission__challenge=challenge) \
                            .values('submission__date', 'submission__user__username',
                                    'f1score', 'submission__simu__name',
                                    'submission__methods', 'submission__level',
                                    'submission__answer', 'submission__with_env_variable',
                                    'submission__desc_method')
    model = results.model
    realheaders = ['submission__date', 'submission__user__username',
                   'f1score', 'submission__simu__name',
                   'submission__methods', 'submission__level','submission__answer',
                   'submission__with_env_variable','submission__desc_method']
    headers = ['Date', 'User', 'Score', 'Dataset', 'Method', 'Level', 'Answer','EnvVar','Desc']
    writer.writerow(headers)

    for res in results:
        row = []
        for field in realheaders:
            val = res.get(field, None)
            
            if callable(val):
                val = val()
            if type(val) == unicode:
                val = val.encode("utf-8")
            row.append(val)
        writer.writerow(row)

    return response

@login_required(login_url='/login/login/')
def challenge_submit(request,challenge_id):

    # render the template with the error
    def render_error(msg_error):
        return render(request, 'challenge/submit.html',
                      {'l_simu': l_simu,
                       'form': form,
                       'challenge': challenge,
                       'error_message': msg_error})

    challenge = Challenge.objects.get(id=challenge_id)
    l_simu = Dataset.objects.filter(challenge__id=challenge_id)

    if request.method == 'POST':
        form = SubmitForm(request.POST,l_simu = l_simu)

        if not request.user.is_authenticated():
            return render_error("You must be logged in.")
            
        if form.is_valid():
            try:
                selected_simu = Dataset.objects.get(name=request.POST['dataset'])
            except (KeyError, Dataset.DoesNotExist):
                return render_error("Wrong selected simulation")

            (soft,desc_soft) = (form.cleaned_data['method'],
                             form.cleaned_data['method_desc'])
            software = soft.name

            nb_submission = Result.objects.filter(submission__challenge=challenge) \
                                          .filter(submission__simu=selected_simu) \
                                          .filter(submission__user=request.user) \
                                          .count()
            maxsubmission = selected_simu.maxsubmission

            if nb_submission >= maxsubmission:
                return render_error("You have already " + str(nb_submission) +
                                    "/" + str(maxsubmission) + " submissions.")

            s = Submission.objects.create(simu=selected_simu,
                                          challenge=challenge,
                                          answer=request.POST['answer'],
                                          date=timezone.now(),
                                          methods=software,
                                          level=Submission.BEGINNER,
                                          with_env_variable=form.cleaned_data['with_environment_variable'],
                                          desc_method=form.cleaned_data['method_desc'],
                                          user=request.user)

            try:
                parsed_answer = s.parse_answer()
            except ValueError:
                return render_error("You must format your answer. For example : 1,2,3")
            else:    
                parsed_truth = selected_simu.parse_truth()

                # TODO : Real F1 score

                truth = set(parsed_truth)
                predicted = set(parsed_answer)

                try:
                    precision = float(len(truth & predicted)) / len(predicted)
                    recall = float(len(truth & predicted)) / len(truth)

                    f1score = 2*precision*recall / (precision + recall)
                except ZeroDivisionError:
                    f1score = 0

                r = Result.objects.create(submission=s,f1score=f1score)

                if selected_simu.private:
                    return render(request, 'challenge/submit.html',
                                  {'l_simu' : l_simu,
                                   'form': form,
                                   'challenge': challenge,
                                   'res': "Submitted !",
                                   'infosubmission': (nb_submission+1,maxsubmission)
                                  })
                else :
                    return render(request, 'challenge/submit.html',
                                  {'l_simu' : l_simu,
                                   'form': form,
                                   'challenge': challenge,
                                   'res': "You obtain a F1 score of " + str(r.f1score),
                                   'infosubmission': [nb_submission+1,maxsubmission]
                               })
            
        else:
            return render_error("Invalid Form")

    else:
        form = SubmitForm(l_simu = l_simu)

    context = {'l_simu': l_simu, 'form': form, 'challenge':challenge}
    return render(request, 'challenge/submit.html', context)


