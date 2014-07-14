from django.shortcuts import render, redirect, HttpResponse
from django.http import Http404
from django.http import HttpResponseNotFound
from django.views.generic import View
from django.views.generic import ListView
from core.forms import AskQuestionForm
from django.views.generic.edit import FormView, ProcessFormView, CreateView

from core.models import Question, User

from rest_framework import viewsets
from core.serializers import QuestionSerializer, UserSerializer

class QuestionView(View):
    model = Question
    def get(self, request, questionid):
        try:
            question = Question.objects.get(pk=questionid)
            question.views += 1;
            question.save()
        except Question.DoesNotExist:
            raise Http404
        return render(request, 'core/question.html', {'question': question})

class UserView(View):
    model = User
    def get(self, request, username):
        try:
            user = User.objects.get(name=username)
        except User.DoesNotExist:
            raise Http404
        return render(request, 'core/user.html', {'user': user})


#TODO: merge with popular view
class QuestionListView(ListView):
    model = Question
    queryset = Question.objects.order_by('-pub_date')

class PopularQuestionListView(ListView):
    model = Question
    queryset = Question.objects.order_by('-rating')

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
        return render(request, 'base.html')


class AskQuestionView(FormView):
    template_name = 'core/new_question.html'
    form_class = AskQuestionForm
    success_url = '/questions'
    def form_valid(self, form):
        form.save()
        return super(AskQuestionView, self).form_valid(form)
