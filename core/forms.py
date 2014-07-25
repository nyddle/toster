# forms.py
from django.db import models
from django import forms
from django.forms import ModelForm

from core.models import Question

class AskQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = [ 'question', 'details', 'tags', 'author', ]

