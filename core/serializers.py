from django.contrib.auth.models import User, Group

from rest_framework import serializers

from .models import Question, MyUser


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyUser
        fields = ('name',)
        lookup_field = 'author'
        view_name = 'user_detail'

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('question', 'author')
