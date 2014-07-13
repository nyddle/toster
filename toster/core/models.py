from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)

class Question(models.Model):
    question = models.CharField(max_length=200)
    #details = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    views = models.IntegerField(default=0)
    answered = models.BooleanField(default=False)
    rating= models.IntegerField(default=0)
    section = models.CharField(max_length=200)
    author = models.ForeignKey(User, default=1)


