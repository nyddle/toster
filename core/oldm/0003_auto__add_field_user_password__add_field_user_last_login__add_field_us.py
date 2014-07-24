# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.password'
        db.add_column('core_user', 'password',
                      self.gf('django.db.models.fields.CharField')(default=1111, max_length=128),
                      keep_default=False)

        # Adding field 'User.last_login'
        db.add_column('core_user', 'last_login',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'User.email'
        db.add_column('core_user', 'email',
                      self.gf('django.db.models.fields.EmailField')(blank=True, max_length=75, null=True),
                      keep_default=False)

        # Adding field 'User.about'
        db.add_column('core_user', 'about',
                      self.gf('django.db.models.fields.TextField')(blank=True, default=''),
                      keep_default=False)

        # Adding unique constraint on 'User', fields ['name']
        db.create_unique('core_user', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'User', fields ['name']
        db.delete_unique('core_user', ['name'])

        # Deleting field 'User.password'
        db.delete_column('core_user', 'password')

        # Deleting field 'User.last_login'
        db.delete_column('core_user', 'last_login')

        # Deleting field 'User.email'
        db.delete_column('core_user', 'email')

        # Deleting field 'User.about'
        db.delete_column('core_user', 'about')


    models = {
        'core.question': {
            'Meta': {'object_name': 'Question'},
            'answered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.User']", 'default': '1'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'core.user': {
            'Meta': {'object_name': 'User'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reg_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'})
        }
    }

    complete_apps = ['core']