from django.shortcuts import render

import json
from datetime import datetime

from challenge.models import Challenge, Dataset, Submission, Result

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

def index(request):
    if request.user.is_authenticated():
        l_results = Result.objects.filter(submission__simu__private=False) \
                                  .filter(submission__user=request.user.id)
        val_results = l_results.values('f1score',
                                       'submission__simu',
                                       'submission__simu__name',
                                       'submission__date')
        context = {'results': l_results,
                   'json_results': json.dumps(list(val_results), default=json_serial)}
        return render(request, 'account/index.html', context)
