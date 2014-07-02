# -*- coding: utf-8 -*-

from datetime import date, timedelta
import csv

from django.contrib import admin
from django.http import HttpResponse
from django.template import Context, Template
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

from .models import Registration

bill_body = Template('''\
Invoice for PyCon Finland {{ year }}

Invoice number: {{ obj.invoice_number }}
Invoice date: {{ obj.bill_date|date }}
Invoice due date: {{ obj.due_date|date }}

Invoice to: {{ obj.name }}{% if obj.company %} / {{ obj.company }}
Address:
{{ obj.billing_address }}

If your company requires the invoice on paper or in some specific format, please contact hallitus@python.fi.
{% endif %}

Description:
------------------------------------------------------------------------
PyCon Finland participant fee: {{ obj.ticket_type|stringformat:"-9s" }}{{ obj.price|stringformat:"28s EUR"}}

------------------------------------------------------------------------
Total: {{ obj.total_price|stringformat:"61s EUR" }}


Please wire {{ obj.total_price }} EUR to following account:

Beneficiary: Python Suomi ry
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


See you at the conference!

Cheers,
PyCon Finland organizers

--
------------------------------------------------------------------------
Python Suomi ry                                       hallitus@python.fi
c/o Tuure Laurinolli                                    http://python.fi

Kasöörinkatu 4 C 50
00520 Helsinki, Finland
------------------------------------------------------------------------
''')

payment_notification_body = Template('''\
Your PyCon Finland {{ year }} bill is overdue. The due date
was {{ obj.due_date|date }}. Please place the payment as soon as
possible.

Here are the bill details again:
{{ obj.bill_text }}
''')

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country',
                    'ticket_type',
                    'billed', 'paid', 'bill_generated', 'bill_overdue',
                    'registered_timestamp')
    list_editable = ('paid',)
    list_filter = ('billed', 'paid',
                   'ticket_type', 'country', 'dinner',
                   'accommodation', 'preconf')
    ordering = ['-registered_timestamp']
    actions = [
        'generate_bill',
        'send_bill',
        'generate_payment_notifiction',
        'send_payment_notification',
        'show_email_addresses',
        'export_as_csv',
    ]

    def bill_overdue(self, obj):
        return (obj.billed and not obj.paid and
                date.today() > obj.bill_date + timedelta(days=14))

    bill_overdue.boolean = True

    def bill_generated(self, obj):
        return obj.bill_text is not None

    bill_overdue.boolean = True

    def send_message(self, conn, subject, body, obj):
        email = EmailMessage(
            subject,
            body,
            bcc=['rahastonhoitaja@python.fi'],
            from_email='Python Suomi ry / '
                       'Rahastonhoitaja <rahastonhoitaja@python.fi>',
            to=[obj.email],
            connection=conn,
        )
        email.send()

    def generate_bill(self, request, queryset):
        for registration in queryset:
            if registration.billed:
                self.message_user(
                    request,
                    'Some of the selected registrations have '
                    'already been billed'
                )
                return

        for registration in queryset:
            registration.bill_date = date.today()
            registration.bill_text = bill_body.render(Context({'obj': obj, 'year': settings.YEAR}))
            registration.save()

    generate_bill.short_description = 'Generate bill text'
        
    def send_bill(self, request, queryset):
        for registration in queryset:
            if registration.billed:
                self.message_user(
                    request,
                    'Some of the selected registrations have '
                    'already been billed'
                )
                return

            if not registration.bill_text:
                self.message_user(
                    request,
                    'Some of the selected registration do not have bill text')
                return

        smtp_connection = get_connection()

        for registration in queryset:
            registration.bill_date = date.today()
            self.send_message(
                smtp_connection,
                'Invoice for PyCon Finland %s' % settings.YEAR,
                registration.bill_text,
                registration,
            )
            registration.billed = True
            registration.save()

    send_bill.short_description = 'Send an e-mail bill'

    def generate_payment_notification(self, request, queryset):
        for registration in queryset:
            if not registration.billed:
                self.message_user(
                    request,
                    'Some of the selected registrations '
                    'have not been billed yet'
                )
                return

            if registration.paid:
                self.message_user(
                    request,
                    'Some of the selected registrations '
                    'have paid'
                )

        for registration in queryset:
            registration.notify_text = payment_notification_body.render(Context({'obj': obj, 'year': settings.YEAR}))
            registration.save()

    send_bill.short_description = 'Generate payment notifications'

    def send_payment_notification(self, request, queryset):
        for registration in queryset:
            if not registration.billed:
                self.message_user(
                    request,
                    'Some of the selected registrations '
                    'have not been billed yet'
                )
                return

            if registration.paid:
                self.message_user(
                    request,
                    'Some of the selected registrations '
                    'have paid'
                )

        smtp_connection = get_connection()

        for registration in queryset:
            self.send_message(
                smtp_connection,
                'Payment notification for PyCon Finland %s' % settings.YEAR,
                registration.notify_text,
                registration,
            )
            registration.notified_date = date.today()
            registration.save()

    def show_email_addresses(self, request, queryset):
        def generate_emails():
            for registration in queryset:
                yield registration.email + '\n'

        return HttpResponse(generate_emails(), mimetype='text/plain')

    show_email_addresses.short_description = (
        'Show email addresses of the selected registrants'
    )

    def export_as_csv(self, request, queryset):
        opts = self.model._meta
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
        )
        writer = csv.writer(response)
        field_names = [field.name for field in opts.fields]
        # Write a first row with header information
        writer.writerow(field_names)
        # Write data rows
        for obj in queryset:
            writer.writerow([
                unicode(getattr(obj, field)).encode('utf-8')
                for field in field_names
            ])
        return response
    export_as_csv.short_description = 'Export registrations as CSV file'

admin.site.register(Registration, RegistrationAdmin)
