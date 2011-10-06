from itertools import izip_longest
from datetime import timedelta
from django.db import models

SEATS_AVAILABLE = 130


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def reference_number(data):
    chk = -sum(int(x) * [7, 3, 1][i % 3] for i, x in enumerate(data[::-1])) % 10
    ref = '%s%d' % (data, chk)
    return ' '.join(reversed([''.join(reversed(x)) for x in grouper(5, reversed(ref), '')]))


class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    ticket_type = models.CharField(max_length=30, choices=(
        ('normal', 'Normal'),
        ('corporate', 'Corporate'),
        ('student', 'Student'),
        ('speaker', 'Speaker'),
        ('sponsor', 'Sponsor'),
        ('organizer', 'Organizer'),
    ))
    country = models.CharField(max_length=2)
    company = models.CharField(max_length=100, null=True, blank=True)

    extra = models.TextField(null=True, blank=True)

    dinner = models.BooleanField(default=True)

    snailmail_bill = models.BooleanField(default=False)
    billing_address = models.CharField(max_length=100, null=True, blank=True)
    billing_zipcode = models.CharField(max_length=15, null=True, blank=True)
    billing_city = models.CharField(max_length=100, null=True, blank=True)

    billed = models.BooleanField(default=False)
    bill_date = models.DateField(null=True, blank=True)
    paid = models.BooleanField(default=False)

    registered_timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def price(self):
        if self.ticket_type == 'corporate':
            return 100
        elif self.ticket_type == 'normal':
            return 50
        elif self.ticket_type == 'student':
            return 10
        else:
            raise ValueError('No price for ticket type %s' % self.ticket_type)

    @property
    def total_price(self):
        if self.snailmail_bill:
            return self.price + 5
        else:
            return self.price

    @property
    def invoice_number(self):
        return self.bill_date.strftime('%Y2') + '%04d' % self.pk

    @property
    def reference_number(self):
        return reference_number(self.invoice_number)

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
