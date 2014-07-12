from django.http import HttpResponse
from django.views.generic import View
from django.views.generic import ListView

from toster.models import Question, User

from rest_framework import viewsets
from toster.serializers import QuestionSerializer, UserSerializer

class QuestionView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')

    def post(self, request):
        # <view logic>
        return HttpResponse('result')

class QuestionListView(ListView):
    model = Question


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


