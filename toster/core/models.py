from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)

class Question(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    views = models.IntegerField()
    answered = models.BooleanField()
    rating= models.IntegerField()
    section = models.CharField(max_length=200)
    author = models.ForeignKey(User)


