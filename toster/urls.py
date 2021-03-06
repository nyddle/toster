from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from rest_framework import routers
from core import views

from django.contrib.auth import get_user_model as user_model
User = user_model()


router = routers.DefaultRouter()
router.register(r'/api/users', views.MyUserViewSet)
router.register(r'/api/questions', views.QuestionViewSet)

urlpatterns = patterns('',
    url(r'^', include('core.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^search/', include('haystack.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # social auth
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^bookmarks/', include('bookmarks.urls')),
    url(r'^likes/', include('likes.urls')),

    url('^activity/', include('actstream.urls')),

    url(r'^avatar/', include('avatar.urls')),
)


