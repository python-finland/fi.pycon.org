from django.http import HttpResponse, HttpResponseNotAllowed

import json
from .forms import RegistrationForm


def register(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = RegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse(json.dumps({'ok': True}))
    else:
        return HttpResponse(json.dumps({'ok': False, 'errors': form.errors}))
