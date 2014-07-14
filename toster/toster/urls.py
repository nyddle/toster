from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from core.views import QuestionView, UserView, QuestionListView, UserListView, HomeView, AskQuestionView

from rest_framework import routers
from core import views

router = routers.DefaultRouter()
router.register(r'/api/users', views.UserViewSet)
router.register(r'/api/questions', views.QuestionViewSet)

urlpatterns = patterns('',
    url(r'^$', QuestionListView.as_view(), name='home'),
    url(r'^home/$', AskQuestionView.as_view(), name='home'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', TemplateView.as_view()),
    url(r'^question/ask', AskQuestionView.as_view(), name='ask_question'),
    url(r'^question/(?P<questionid>.+)', QuestionView.as_view(), name='question'),
    url(r'^user/(?P<username>.+)', UserView.as_view(), name='user'),
    url(r'^questions/$', QuestionListView.as_view(), name='questions'),
    url(r'^users/$', UserListView.as_view(), name='users'),
)


