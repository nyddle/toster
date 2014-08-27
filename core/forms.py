# forms.py
from django.db import models
from django import forms
from django.forms import ModelForm

from core.models import Question, UserProfile

class AskQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = [ 'question', 'details', 'tags', 'author', ]


class EditProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'about', 'user_avatar']