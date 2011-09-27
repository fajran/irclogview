# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Channel'
        db.create_table('irclogview_channel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('irclogview', ['Channel'])

        # Adding model 'Log'
        db.create_table('irclogview_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['irclogview.Channel'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('mtime', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('content', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('irclogview', ['Log'])

        # Adding unique constraint on 'Log', fields ['channel', 'date']
        db.create_unique('irclogview_log', ['channel_id', 'date'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Log', fields ['channel', 'date']
        db.delete_unique('irclogview_log', ['channel_id', 'date'])

        # Deleting model 'Channel'
        db.delete_table('irclogview_channel')

        # Deleting model 'Log'
        db.delete_table('irclogview_log')


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
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtime': ('django.db.models.fields.DateTimeField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['irclogview']
