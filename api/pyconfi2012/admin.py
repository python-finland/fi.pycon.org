# -*- coding: utf-8 -*-

from datetime import date, timedelta

from django.contrib import admin
from django.http import HttpResponse
from django.template import Context, Template
from django.core.mail import EmailMessage, get_connection
from .models import Registration
from django.core.mail import send_mail

bill_body = Template('''\
Billing information for PyCon Finland 2012

Invoice number: {{ obj.invoice_number }}
Invoice date: {{ obj.bill_date|date }}
Invoice due date: {{ obj.due_date|date }}
Invoice to: {{ obj.name }}{% if obj.company %}
Company: {{ obj.company }}{% endif %}

Description:
------------------------------------------------------------------------
PyCon Finland participant fee: {{ obj.ticket_type|stringformat:"-9s" }}{{ obj.price|stringformat:"28s EUR"}}{% if obj.snailmail_bill %}
Paper bill: {{ "5 EUR"|stringformat:"60s"}}{% endif %}

------------------------------------------------------------------------
Total: {{ obj.total_price|stringformat:"61s EUR" }}


Please wire {{ obj.total_price }} EUR to following account:

Beneficary: Python Suomi ry
Bank: Aktia Oyj
IBAN: FI27 4055 0011 0236 33
BIC: HELSFIHH
Reference (viitenumero): {{ obj.reference_number }}

DUE DATE: {{ obj.due_date|date }}

Make sure to use the correct reference when paying. Please note that
all prices are VAT exempt (in Finnish: Lasku ei sisällä vähennettävää
arvonlisäveroa)

If there's anything you'd like to ask about billing, don't hesitate to
contact hallitus@python.fi.


See you in the conference!

Cheers,
PyCon Finland organizers

-- 
------------------------------------------------------------------------
Python Suomi ry                                       hallitus@python.fi
c/o Joni Orponen, Dodreams Ltd.                         http://python.fi

Erottajankatu 15-17 A 7th floor
00130 Helsinki, Finland
------------------------------------------------------------------------
''')

payment_notification_body = Template('''\
You're PyCon Finland 2012 bill is overdue. The due date
was {{ obj.due_date|date }}. Please place the payment as soon as
possible.

Here are the bill details again:

Invoice number: {{ obj.invoice_number }}
Invoice date: {{ obj.bill_date|date }}
Invoice due date: {{ obj.due_date|date }}
Invoice to: {{ obj.name }}{% if obj.company %}
Company: {{ obj.company }}{% endif %}

Description:
------------------------------------------------------------------------
PyCon Finland participant fee: {{ obj.ticket_type|stringformat:"-9s" }}{{ obj.price|stringformat:"28s EUR"}}{% if obj.snailmail_bill %}
Paper bill: {{ "5 EUR"|stringformat:"60s"}}{% endif %}

------------------------------------------------------------------------
Total: {{ obj.total_price|stringformat:"61s EUR" }}


Please wire {{ obj.total_price }} EUR to following account:

Beneficary: Python Suomi ry
Bank: Aktia Oyj
IBAN: FI27 4055 0011 0236 33
BIC: HELSFIHH
Reference (viitenumero): {{ obj.reference_number }}

Make sure to use the correct reference when paying. Please note that
all prices are VAT exempt (in Finnish: Lasku ei sisällä vähennettävää
arvonlisäveroa)

If there's anything you'd like to ask about billing, don't hesitate to
contact hallitus@python.fi.


See you in the conference!

Cheers,
PyCon Finland organizers

-- 
------------------------------------------------------------------------
Python Suomi ry                                       hallitus@python.fi
c/o Jyrki Pulliainen                                    http://python.fi
Vartiokuja 1 E 37
20700 Turku, Finland
------------------------------------------------------------------------
''')

confirmation_email_body = Template('''\
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
Radisson Blu Hotel Espoo (http://www.radissonblu.fi/hotelli-espoo). Using code PYTHON you get discount prices
for single and double rooms.    

You will receive a bill in a separate email closer to the event.

The registration can be cancelled by contacting
hallitus@python.fi. 25 EUR cancellation fee until and including
September 30th. No return after September 30th.

See you in PyCon Finland 2012!

Best regards,
Organizers

''')

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country',
                    'ticket_type', 'snailmail_bill',
                    'billed', 'paid', 'bill_overdue',
                    'registered_timestamp')
    list_editable = ('paid',)
    list_filter = ('snailmail_bill', 'billed', 'paid',
                   'ticket_type', 'country', 'dinner', 
                   'accommodation', 'preconf')
    ordering = ['-registered_timestamp']
    actions = ['send_bill', 'send_payment_notification', 'show_email_addresses',       'send_confirmation_email']

    def bill_overdue(self, obj):
        return (obj.billed and not obj.paid and
                date.today() > obj.bill_date + timedelta(days=14))

    bill_overdue.boolean = True

    def send_message(self, conn, subject, body_template, obj):
        email = EmailMessage(
            subject,
            body_template.render(Context({'obj': obj})),
            bcc=['taloudenhoitaja@python.fi'],
            from_email='Python Suomi ry / Taloudenhoitaja <taloudenhoitaja@python.fi>',
            to=[obj.email],
            connection=conn,
        )
        email.send()

    def send_bill(self, request, queryset):
        for registration in queryset:
            if registration.billed:
                self.message_user(request, 'Some of the selected registrations '
                                  'have already been billed')
                return

            if registration.snailmail_bill:
                self.message_user(request, 'Some of the selected registrations '
                                  'shuld be billed via snail mail')

        smtp_connection = get_connection()

        for registration in queryset:
            registration.bill_date = date.today()
            self.send_message(
                smtp_connection,
                'Invoice for PyCon Finland 2012',
                bill_body,
                registration,
            )
            registration.billed = True
            registration.save()

    send_bill.short_description = 'Send an e-mail bill'

    def send_payment_notification(self, request, queryset):
        for registration in queryset:
            if not registration.billed:
                self.message_user(request, 'Some of the selected registrations '
                                  'have not been billed yet')
                return

            if registration.snailmail_bill:
                self.message_user(request, 'Some of the selected registrations '
                                  'should be billed via snail mail')

        smtp_connection = get_connection()

        for registration in queryset:
            self.send_message(
                smtp_connection,
                'Payment notification for PyCon Finland 2012',
                payment_notification_body,
                registration,
            )
            registration.notified_date = date.today()
            registration.save()

    def show_email_addresses(self, request, queryset):
        def generate_emails():
            for registration in queryset:
                yield registration.email + '\n'

        return HttpResponse(generate_emails(), mimetype='text/plain')

    show_email_addresses.short_description = ('Show email addresses of the '
                                              'selected registrants')

    def send_confirmation_email(self, request, queryset):
        smtp_connection = get_connection()

        for registration in queryset:
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
                confirmation_email_body.render(Context({
                    'x': registration,
                    'price': price,
                    })),
                'hallitus@python.fi',
                [u'%s <%s>' % (registration.name, registration.email)],
            )
    send_confirmation_email.short_description = 'Send confirmation email'

admin.site.register(Registration, RegistrationAdmin)
