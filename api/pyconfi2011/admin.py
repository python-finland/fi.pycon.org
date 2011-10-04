# -*- coding: utf-8 -*-

from datetime import date

from django.contrib import admin
from django.http import HttpResponse
from django.template import Context, Template
from django.core.mail import EmailMessage, get_connection
from .models import Registration

bill_body = Template('''\
Billing information for PyCon Finland 2011

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
c/o Jyrki Pulliainen                                    http://python.fi
Vartiokuja 1 E 37
20700 Turku, Finland
------------------------------------------------------------------------
''')


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country',
                    'ticket_type', 'snailmail_bill',
                    'billed', 'paid', 'registered_timestamp')
    list_editable = ('paid',)
    list_filter = ('snailmail_bill', 'billed', 'paid',
                   'ticket_type', 'country', 'dinner')
    ordering = ['-registered_timestamp']
    actions = ['send_bill', 'show_email_addresses']

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
            email_body = bill_body.render(Context({'obj': registration}))
            email_subject = 'Invoice for PyCon Finland 2011'

            email = EmailMessage(
                email_subject,
                email_body,
                bcc=['taloudenhoitaja@python.fi'],
                from_email='Python Suomi ry / Taloudenhoitaja <taloudenhoitaja@python.fi>',
                to=[registration.email],
                connection=smtp_connection,
            )

            email.send()
            registration.billed = True
            registration.save()

    send_bill.short_description = ('Send an e-mail bill to the '
                                   'selected registrants')

    def show_email_addresses(self, request, queryset):
        def generate_emails():
            for registration in queryset:
                yield registration.email + '\n'

        return HttpResponse(generate_emails(), mimetype='text/plain')

    show_email_addresses.short_description = ('Show email addresses of the '
                                              'selected registrants')


admin.site.register(Registration, RegistrationAdmin)
