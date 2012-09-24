import os

from django.http import HttpResponse
from django.core.mail import send_mail
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

import json
from .forms import RegistrationForm, COUNTRIES
from .models import Registration, SEATS_AVAILABLE

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
    Radisson Blu Hotel Espoo. Using code PYTHON you get discount prices
    for single and double rooms.    

    You will receive a bill in a separate email closer to the event.

    The registration can be cancelled by contacting
    hallitus@python.fi. 25 EUR cancellation fee until and including
    September 30th. No return after September 30th.

    See you in PyCon Finland 2012!

    Best regards,
    Organizers

                      ''')


def send_confirmation_email(registration):
    if registration.ticket_type == 'corporate':
        price = 125
    elif registration.ticket_type == 'normal':
        price = 50
    elif registration.ticket_type == 'student':
        price = 10

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
    if Registration.objects.count() >= SEATS_AVAILABLE:
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
    count = SEATS_AVAILABLE - Registration.objects.count()
    return HttpResponse(json.dumps({'ok': True, 'count': count}))


@require_GET
def autocomplete_country(request):
    results = []
    for name, code in COUNTRIES:
        if request.GET.get('query').lower() in name.lower():
            results.append(name)
    return HttpResponse(json.dumps(results))

# index.html hack

def index(request):
    from django.template import loader
    t = loader.get_template("index.html")
    c = Context({})
    return HttpResponse(t.render(c))

