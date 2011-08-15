from django.db import models


class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    ticket_type = models.CharField(max_length=30, choices=(
        ('normal', 'Normal'),
        ('corporate', 'Corporate'),
        ('student', 'Student'),
    ))
    country = models.CharField(max_length=2)

    dinner = models.BooleanField(default=True)

    snailmail_bill = models.BooleanField(default=False)
    billing_address = models.CharField(max_length=100)
    billing_zipcode = models.CharField(max_length=15)
    billing_city = models.CharField(max_length=100)

    billed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
