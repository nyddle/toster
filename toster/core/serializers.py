from django.contrib.auth.models import User, Group
from rest_framework import serializers
from toster.models import Question, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('name',)
        lookup_field = 'author'
        view_name = 'user_detail'

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('question', 'author')
