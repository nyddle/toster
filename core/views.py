from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from django.http import Http404
from django.http import HttpResponseNotFound

from django.views.generic import View
from django.views.generic import ListView
from django.views.generic.edit import FormView, ProcessFormView, CreateView

from rest_framework import viewsets

from .forms import AskQuestionForm
from .models import Question, MyUser
from .serializers import QuestionSerializer, MyUserSerializer

from taggit.models import Tag

from bookmarks.handlers import library
from bookmarks.models import Bookmark

from django.contrib.auth import get_user_model as user_model

from actstream import action
from actstream.models import model_stream, any_stream

class FeedView(View):

    def get(self, request):
        return render(request, 'core/feed.html', { 'stream' : any_stream(request.user) })

class QuestionView(View):
    model = Question

    def get(self, request, questionid, slug):
        try:
            question = Question.objects.get(pk=questionid)
        except Question.DoesNotExist:
            raise Http404
        question.views += 1
        question.save()

        return render(request, 'core/question.html', {'question': question})


class MyUserView(View):
    model = MyUser

    def get(self, request, username):
        try:
            user = MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            raise Http404
        return render(request, 'core/user.html', {'user': user})


#TODO: merge with popular view
class QuestionListView(ListView):
    model = Question
    queryset = Question.objects.order_by('-pub_date')

    def get_queryset(self):
        queryset = super(QuestionListView, self).get_queryset()
        if 'tag' in self.kwargs:
            tag = self.kwargs['tag']
            return queryset.filter(tags__name__in=[tag,])
        q = self.request.GET.get("q")
        if q:
            return queryset.filter(question__icontains=q)
        return queryset


class PopularQuestionListView(ListView):
    model = Question
    queryset = Question.objects.order_by('-rating')


class MyUserListView(ListView):
    model = MyUser


class MyUserQuestionListView(ListView):
    model = Question

    def get_queryset(self):
        self.author = get_object_or_404(MyUser, name=self.kwargs['username'])
        return Question.objects.filter(author=self.author)


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class MyUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


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


class TagListView(ListView):
    model = Tag


#TODO: MembersView?
class Members(View):
    def get(self, request):
        print('user', request.user)
        print('session', request.session.keys())
        return render(request, 'core/member.html')


class BookmarksView(View):

    def get(self, request):
        bookmarks = Bookmark.objects.filter_with_contents(user=self.request.user)
        return render(request, 'core/bookmark_list.html', { 'bookmarks' : bookmarks })
