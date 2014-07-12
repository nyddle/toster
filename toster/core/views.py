from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseNotFound
from django.views.generic import View
from django.views.generic import ListView

from core.models import Question, User

from rest_framework import viewsets
from core.serializers import QuestionSerializer, UserSerializer

class QuestionView(View):
    model = Question
    def get(self, request, questionid):
        try:
            question = Question.objects.get(pk=questionid)
        except:
            raise Http404
        return render(request, 'core/question.html', { 'question' : question })

class UserView(View):
    #self.kwargs['year']
    def get(self, request):
        return HttpResponse('result')

    def post(self, request):
        return HttpResponse('result')

class QuestionListView(ListView):
    model = Question

class UserListView(ListView):
    model = User


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HomeView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')

    def post(self, request):
        # <view logic>
        return HttpResponse('result')
