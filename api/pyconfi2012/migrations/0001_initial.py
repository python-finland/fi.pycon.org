# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Registration'
        db.create_table('pyconfi2012_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('ticket_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('extra', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dinner', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('snailmail_bill', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('billing_address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('billing_zipcode', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('billing_city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('billed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bill_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('notified_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('registered_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('pyconfi2012', ['Registration'])


    def backwards(self, orm):
        
        # Deleting model 'Registration'
        db.delete_table('pyconfi2012_registration')


    models = {
        'pyconfi2012.registration': {
            'Meta': {'object_name': 'Registration'},
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
            'registered_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'snailmail_bill': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ticket_type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['pyconfi2012']
