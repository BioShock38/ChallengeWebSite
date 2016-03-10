from django.shortcuts import render

from challenge.models import Challenge, Dataset, Submission, Result

def index(request):
    if request.user.is_authenticated():
        l_results = Result.objects.filter(submission__simu__private=False) \
                                  .filter(submission__user=request.user.id)
        context = {'results': l_results}
        return render(request, 'account/index.html', context)
