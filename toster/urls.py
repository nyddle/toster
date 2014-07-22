from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from rest_framework import routers
from core import views

router = routers.DefaultRouter()
router.register(r'/api/users', views.UserViewSet)
router.register(r'/api/questions', views.QuestionViewSet)

urlpatterns = patterns('',
    url(r'^', include('core.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^search/', include('haystack.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # social auth
    url(r'', include('social_auth.urls')),

)


