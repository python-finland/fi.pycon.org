from django.contrib import admin
from django.template import Template
from .models import Registration

email_body = Template('''\
Billing information for PyCon Finland 2011

Invoice number: {{ reference }}
Invoice date: {{ date }}
Invoice due date: {{ due_date }}
Invoice to: {{ name }}
{% if company %}}Company: {{ company }}{% endif %}


Description
------------------------------------------------------------------------
PyCon Finland participant fee: {{ ticket_type|stringformat "%-9s" }}{{ price|stringformat "%32s"}}
{% if snailmail_bill %}Paper bill{{ "5 EUR"|stringformat "%62s"}}{%endif%}}

------------------------------------------------------------------------
Total:{{ obj.total_price|stringformat "%66s" }}


Please wire {{ obj.total_price }} to following account:

Beneficary: Python Suomi ry
Bank: Aktia Oyj
IBAN: FI27 4055 0011 0236 33
BIC: HELSFIHH
Reference (viitenumero): {{ obj.reference }}

DUE DATE: {{ due_date }}

Make sure to use the correct reference when paying.

If there's anything you'd like to ask about billing, don't hesitate to
contact hallitus@python.fi.


See you in the conference!

Cheers,
The PyCon Finland organizers

------------------------------------------------------------------------
Python Suomi ry                                       hallitus@python.fi
c/o Jyrki Pulliainen                                    http://python.fi
Vartiokuja 1 E 37
20700 Turku, Finland
------------------------------------------------------------------------

''')


def reference_number(s):
    return '%s%d' % (s, -sum(int(x) * [7, 3, 1][i % 3]
                        for i, x in enumerate(s[::-1])) % 10)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country',
                    'ticket_type', 'billed', 'paid',
                    'registered_timestamp')
    list_editable = ('paid',)
    list_filter = ('billed', 'paid', 'ticket_type', 'country')
    ordering = ['-registered_timestamp']
    actions = ['send_bill']

    def send_bill(self, request, queryset):
        pass

    send_bill.short_description = ('Send an e-mail bill to the '
                                   'selected registrants')


admin.site.register(Registration, RegistrationAdmin)
