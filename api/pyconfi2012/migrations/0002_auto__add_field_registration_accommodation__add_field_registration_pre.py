# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Registration.accommodation'
        db.add_column('pyconfi2012_registration', 'accommodation', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Registration.preconf'
        db.add_column('pyconfi2012_registration', 'preconf', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Registration.accommodation'
        db.delete_column('pyconfi2012_registration', 'accommodation')

        # Deleting field 'Registration.preconf'
        db.delete_column('pyconfi2012_registration', 'preconf')


    models = {
        'pyconfi2012.registration': {
            'Meta': {'object_name': 'Registration'},
            'accommodation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bill_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billing_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'billing_city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'billing_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'dinner': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notified_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'preconf': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'registered_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'snailmail_bill': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ticket_type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['pyconfi2012']
