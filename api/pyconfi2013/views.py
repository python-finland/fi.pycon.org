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
    Thanks for registering to PyCon Finland 2012!

    Here's your registration info:
    {% autoescape off %}
    Name: {{ x.name }}
    E-mail: {{ x.email }}
    Ticket type: {{ x.ticket_type }}{% if x.ticket_type == "corporate" %}
    Company: {{ x.company }}
    Dinner: {{ x.dinner|yesno:"yes,no" }}{% endif %}
    Paper bill: {{ x.snailmail_bill|yesno:"yes,no" }}{% if x.snailmail_bill %}
    Billing address: {{ x.billing_address }}, {{ x.billing_zipcode }} {{ x.billing_city}}{% endif %}{% if x.extra %}
    Additional info:
    {{ x.extra }}{% endif %}

    Total price: {{ price }} EUR
    {% endautoescape %}
    If there's anything wrong with the information above, please contact
    hallitus@python.fi to resolve the issue.
    
    If you're in need of accommodation, we have a special deal with 
    Radisson Blu Hotel Espoo (http://www.radissonblu.fi/hotelli-espoo). 
    Using code PYTHON you get discount prices
    for single and double rooms.

    {% if x.ticket_type == "corporate" or x.ticket_type == "normal" or x.ticket_type == "student" %}
    You will receive a bill in a separate email closer to the event.

    The registration can be cancelled by contacting
    hallitus@python.fi. 25 EUR cancellation fee until and including
    September 30th. No return after September 30th.
    {% endif %}
    See you in PyCon Finland 2012!

    Best regards,
    Organizers

''')


def send_confirmation_email(registration):
    ticket_type = registration.ticket_type
    if ticket_type in settings.TICKET_PRICES:
        price = settings.TICKET_PRICES[ticket_type]
    else:
        raise ValueError('No price for ticket type %s' % ticket_type)

    if registration.snailmail_bill:
        price += 5

    send_mail(
        'Your registration to PyCon Finland 2012',
        email_body.render(Context({
            'x': registration,
            'price': price,
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
        form.save()
        send_confirmation_email(form.instance)
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
