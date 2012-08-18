# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Registration.dinner'
        db.add_column('pyconfi2012_registration', 'dinner', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'Registration.billing_address'
        db.add_column('pyconfi2012_registration', 'billing_address', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)

        # Adding field 'Registration.billing_zipcode'
        db.add_column('pyconfi2012_registration', 'billing_zipcode', self.gf('django.db.models.fields.CharField')(default='', max_length=15), keep_default=False)

        # Adding field 'Registration.billing_city'
        db.add_column('pyconfi2012_registration', 'billing_city', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)

        # Adding field 'Registration.country'
        db.add_column('pyconfi2012_registration', 'country', self.gf('django.db.models.fields.CharField')(default='', max_length=2), keep_default=False)

        # Adding field 'Registration.billed'
        db.add_column('pyconfi2012_registration', 'billed', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Registration.paid'
        db.add_column('pyconfi2012_registration', 'paid', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Changing field 'Registration.ticket_type'
        db.alter_column('pyconfi2012_registration', 'ticket_type', self.gf('django.db.models.fields.CharField')(max_length=30))


    def backwards(self, orm):
        
        # Deleting field 'Registration.dinner'
        db.delete_column('pyconfi2012_registration', 'dinner')

        # Deleting field 'Registration.billing_address'
        db.delete_column('pyconfi2012_registration', 'billing_address')

        # Deleting field 'Registration.billing_zipcode'
        db.delete_column('pyconfi2012_registration', 'billing_zipcode')

        # Deleting field 'Registration.billing_city'
        db.delete_column('pyconfi2012_registration', 'billing_city')

        # Deleting field 'Registration.country'
        db.delete_column('pyconfi2012_registration', 'country')

        # Deleting field 'Registration.billed'
        db.delete_column('pyconfi2012_registration', 'billed')

        # Deleting field 'Registration.paid'
        db.delete_column('pyconfi2012_registration', 'paid')

        # Changing field 'Registration.ticket_type'
        db.alter_column('pyconfi2012_registration', 'ticket_type', self.gf('django.db.models.fields.CharField')(max_length='30'))


    models = {
        'pyconfi2012.registration': {
            'Meta': {'object_name': 'Registration'},
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billing_address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'billing_city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'billing_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'dinner': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ticket_type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['pyconfi2012']
