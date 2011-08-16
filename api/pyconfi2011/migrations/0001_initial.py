# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Registration'
        db.create_table('pyconfi2011_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('ticket_type', self.gf('django.db.models.fields.CharField')(max_length='30')),
        ))
        db.send_create_signal('pyconfi2011', ['Registration'])


    def backwards(self, orm):
        
        # Deleting model 'Registration'
        db.delete_table('pyconfi2011_registration')


    models = {
        'pyconfi2011.registration': {
            'Meta': {'object_name': 'Registration'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ticket_type': ('django.db.models.fields.CharField', [], {'max_length': "'30'"})
        }
    }

    complete_apps = ['pyconfi2011']
