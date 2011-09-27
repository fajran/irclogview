# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'Log', fields ['date']
        db.create_index('irclogview_log', ['date'])


    def backwards(self, orm):
        
        # Removing index on 'Log', fields ['date']
        db.delete_index('irclogview_log', ['date'])


    models = {
        'irclogview.channel': {
            'Meta': {'ordering': "['name']", 'object_name': 'Channel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'irclogview.log': {
            'Meta': {'ordering': "['-date']", 'unique_together': "(('channel', 'date'),)", 'object_name': 'Log'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['irclogview.Channel']"}),
            'content': ('picklefield.fields.PickledObjectField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtime': ('django.db.models.fields.DateTimeField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['irclogview']
