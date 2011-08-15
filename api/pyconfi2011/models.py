from django.db import models


class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    ticket_type = models.CharField(max_length='30', choices=(
        ('normal', 'Normal'),
        ('corporate', 'Corporate'),
        ('student', 'Student'),
    ))
