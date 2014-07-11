from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from toster.views import QuestionView, QuestionListView

from rest_framework import routers
from toster import views

router = routers.DefaultRouter()
router.register(r'questions', views.UserViewSet)
router.register(r'questions', views.QuestionViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'toster.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', TemplateView.as_view()),
    url(r'^question/', QuestionView.as_view()),
)

#url(r'^questions/', QuestionListView.as_view()),

