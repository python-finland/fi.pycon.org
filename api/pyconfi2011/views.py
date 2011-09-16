from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.mail import send_mail
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt

import json
from .forms import RegistrationForm

email_body = Template('''\
Thanks for registering to PyCon Finland 2011!

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

You will receive a bill in a separate email closer to the event.

The registration can be cancelled by contacting hallitus@python.fi.
Full return, 25 EUR cancellation fee until September 15th. No return
after September 15th.

See you in PyCon Finland 2011!

Best regards,
Organizers
''')


def send_confirmation_email(registration):
    if registration.ticket_type == 'corporate':
        price = 100
    elif registration.ticket_type == 'normal':
        price = 50
    elif registration.ticket_type == 'student':
        price = 10

    if registration.snailmail_bill:
        price += 5

    send_mail(
        'Your registration to PyCon Finland 2011',
        email_body.render(Context({
            'x': registration,
            'price': price,
        })),
        'hallitus@python.fi',
        [u'%s <%s>' % (registration.name, registration.email)],
    )


@csrf_exempt
def register(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = RegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        send_confirmation_email(form.instance)
        return HttpResponse(json.dumps({'ok': True}))
    else:
        return HttpResponse(json.dumps({'ok': False, 'errors': form.errors}))
