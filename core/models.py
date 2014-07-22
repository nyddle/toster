from django.db import models
from taggit.managers import TaggableManager

import secretballot

class User(models.Model):
    name = models.CharField(max_length=200)
    reg_date = models.DateTimeField('date registered', auto_now_add=True)
    rating = models.IntegerField(default=0)
    #about = models.CharField(max_length=1000)


class Question(models.Model):
    question = models.CharField(max_length=200)
    details = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    views = models.IntegerField(default=0)
    answered = models.BooleanField(default=False)
    rating= models.IntegerField(default=0)
    section = models.CharField(max_length=200)
    author = models.ForeignKey(User, default=1)
    tags = TaggableManager()

secretballot.enable_voting_on(Question)

