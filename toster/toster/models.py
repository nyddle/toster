from django.db import models

class Question(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    poll = models.ForeignKey(User)

class User(models.Model):
    name = models.CharField(max_length=200)

