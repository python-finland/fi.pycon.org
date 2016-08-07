from django.db import models
from django.conf import settings

from itertools import izip_longest
from datetime import timedelta


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def reference_number(data):
    chk = -sum(
        int(x) * [7, 3, 1][i % 3] for i, x in enumerate(data[::-1])
    ) % 10
    ref = '%s%d' % (data, chk)
    return ' '.join(reversed(
        [''.join(reversed(x)) for x in grouper(5, reversed(ref), '')]
    ))

def is_corporate(ticket_type):
    return ticket_type.startswith('corporate')

def virtual_barcode_4(price, due_date, reference_number):
    cents = "%08d" %(price*100)
    refnum = ("%20s" % reference_number.replace(" ", "")).replace(" ", "0")
    duedate = due_date.strftime("%y%m%d")
    return '4' + '2740550011023633' + cents + "000" + refnum + duedate;

class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    ticket_type = models.CharField(max_length=30, choices=(
            ('individual_eb', 'Individual Early Bird'),
            ('individual', 'Individual'),
            ('corporate_eb', 'Corporate Early Bird'),
            ('corporate', 'Corporate'),
            ('student', 'Student'),
            ('organizer', 'Organizer'),
            ('speaker', 'Speaker'),
            ('sponsor', 'Sponsor')
    ))
    country = models.CharField(max_length=2)
    company = models.CharField(max_length=100, null=True, blank=True)

    extra = models.TextField(null=True, blank=True)

    dinner = models.BooleanField(default=True)
    preconf = models.BooleanField()

    confirmation_sent = models.BooleanField(default=False)

    billing_address = models.TextField(null=True, blank=True)

    billed = models.BooleanField(default=False)
    bill_date = models.DateField(null=True, blank=True)
    bill_text = models.TextField(null=True, blank=True)
    notified_date = models.DateField(null=True, blank=True)
    notify_text = models.TextField(null=True, blank=True)
    paid = models.BooleanField(default=False)

    registered_timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def price(self):
        ticket_type = self.ticket_type
        if ticket_type in settings.TICKET_PRICES:
            return settings.TICKET_PRICES[ticket_type]
        else:
            raise ValueError('No price for ticket type %s' % ticket_type)

    @property
    def total_price(self):
        return self.price

    @property
    def invoice_number(self):
        return self.bill_date.strftime('%Y2') + '%04d' % self.pk

    @property
    def reference_number(self):
        return reference_number(self.invoice_number)

    @property
    def barcode(self):
        return virtual_barcode_4(self.price, self.due_date, self.reference_number)

    @property
    def due_date(self):
        return self.bill_date + timedelta(days=14)

    def __unicode__(self):
        return u'%s, %s, %s, %s, %s' % (
            self.name,
            self.email,
            self.country,
            self.ticket_type,
            self.registered_timestamp.strftime('%c'),
        )
