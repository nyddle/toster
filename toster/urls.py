from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from core.views import HomeView, QuestionView, UserView, QuestionListView, PopularQuestionListView, \
                        UserListView, AskQuestionView, UserView, UserQuestionListView

from rest_framework import routers
from core import views

router = routers.DefaultRouter()
router.register(r'/api/users', views.UserViewSet)
router.register(r'/api/questions', views.QuestionViewSet)

urlpatterns = patterns('',

    url(r'^$', QuestionListView.as_view(), name='home'),
    url(r'^question/ask', AskQuestionView.as_view(), name='ask_question'),
    url(r'^question/(?P<questionid>.+)', QuestionView.as_view(), name='question'),

    url(r'^questions/latest/$', QuestionListView.as_view(), name='questions_latest'),
    url(r'^questions/popular/$', PopularQuestionListView.as_view(), name='questions_popular'),
    url(r'^questions/$', QuestionListView.as_view(), name='questions'),
    url(r'^user/(?P<username>.+)/questions', UserQuestionListView.as_view(), name='user_questions'),

    url(r'^user/(?P<username>.+)', UserView.as_view(), name='user'),
    url(r'^users/$', UserListView.as_view(), name='users'),

    url(r'^home/$', AskQuestionView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name='about'),

    url(r'^search2/$', QuestionListView.as_view(), name='search_results'),
    url(r'^search/', include('haystack.urls')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

)


