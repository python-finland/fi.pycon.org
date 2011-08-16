# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Registration.extra'
        db.add_column('pyconfi2011_registration', 'extra', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Changing field 'Registration.billing_address'
        db.alter_column('pyconfi2011_registration', 'billing_address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Registration.billing_zipcode'
        db.alter_column('pyconfi2011_registration', 'billing_zipcode', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

        # Changing field 'Registration.billing_city'
        db.alter_column('pyconfi2011_registration', 'billing_city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))


    def backwards(self, orm):
        
        # Deleting field 'Registration.extra'
        db.delete_column('pyconfi2011_registration', 'extra')

        # User chose to not deal with backwards NULL issues for 'Registration.billing_address'
        raise RuntimeError("Cannot reverse this migration. 'Registration.billing_address' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Registration.billing_zipcode'
        raise RuntimeError("Cannot reverse this migration. 'Registration.billing_zipcode' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Registration.billing_city'
        raise RuntimeError("Cannot reverse this migration. 'Registration.billing_city' and its values cannot be restored.")


    models = {
        'pyconfi2011.registration': {
            'Meta': {'object_name': 'Registration'},
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billing_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'billing_city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'billing_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'dinner': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'snailmail_bill': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ticket_type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['pyconfi2011']
