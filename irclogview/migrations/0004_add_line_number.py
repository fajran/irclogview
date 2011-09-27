# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Bookmark.line'
        db.add_column('irclogview_bookmark', 'line', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Bookmark.line'
        db.delete_column('irclogview_bookmark', 'line')


    models = {
        'irclogview.bookmark': {
            'Meta': {'object_name': 'Bookmark'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['irclogview.Log']"}),
            'path': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
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
