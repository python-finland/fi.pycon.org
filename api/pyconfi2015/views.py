from django.http import HttpResponse
from django.core.mail import send_mail
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.shortcuts import render

from .forms import RegistrationForm, COUNTRIES
from .models import Registration

import json

email_body = Template('''\
    Thanks for registering to PyCon Finland {{ year }}!

    Here's your registration info:
    {% autoescape off %}
    Name: {{ x.name }}
    E-mail: {{ x.email }}
    Ticket type: {{ x.ticket_type }}{% if "corporate" in x.ticket_type %}
    Company: {{ x.company }}
    
    Dinner: {{ x.dinner|yesno:"yes,no" }}{% endif %}
    {% if "corporate" in x.ticket_type %}
    Billing address:
    {{ x.billing_address }}{% endif %}{% if x.extra %}
    Additional info:
    {{ x.extra }}{% endif %}

    Total price: {{ x.total_price }} EUR
    {% endautoescape %}
    If there's anything wrong with the information above, please contact
    hallitus@python.fi to resolve the issue.

    {% if "corporate" in x.ticket_type or "individual" in x.ticket_type or x.ticket_type == "student" %}
    You will receive an invoice in a separate email. Don't be alarmed
    if you haven't received an invoice before the event, as we may
    only be able to send them out afterwards, especially for late
    registrants.

    The registration can be cancelled by contacting
    hallitus@python.fi. 25 EUR cancellation fee applies until and including
    September 30th. After September 30th cancellation is not possible.

    Note that you can transfer your registration to another person
    until the very morning of the event! If you want to do this, please
    contact hallitus@python.fi so that we know whom to expect in your stead.

    {% endif %}
    See you at PyCon Finland {{ year }}!

    Best regards,
    Organizers

''')


def send_confirmation_email(registration):

    send_mail(
        'Your registration to PyCon Finland %s' % settings.YEAR,
        email_body.render(Context({
            'x': registration,
            'year': settings.YEAR,
        })),
        'hallitus@python.fi',
        [u'%s <%s>' % (registration.name, registration.email)],
    )


@csrf_exempt
@require_POST
def register(request):
    if Registration.objects.count() >= settings.SEATS_AVAILABLE:
        return HttpResponse(json.dumps({
            'ok': False,
            'errors': {
                '__all__': 'No seats left'
            },
        }))

    form = RegistrationForm(request.POST)
    if form.is_valid():
        m = form.save()
        send_confirmation_email(form.instance)
        m.confirmation_sent = True
        m.save()
        return HttpResponse(json.dumps({'ok': True}))
    else:
        return HttpResponse(json.dumps({'ok': False, 'errors': form.errors}))
    return HttpResponse(json.dumps({'ok': True}))


@require_GET
def seats_left(request):
    count = settings.SEATS_AVAILABLE - Registration.objects.count()
    return HttpResponse(json.dumps({'ok': True, 'count': count}))


@require_GET
def autocomplete_country(request):
    results = []
    for name, code in COUNTRIES:
        if (
            request.GET.get('query')
            and request.GET.get('query').lower() in name.lower()
        ):
            results.append(name)
    return HttpResponse(json.dumps(results))


# some hacking to get empty template
def index(request):
    return render(request, 'index.html', {})
