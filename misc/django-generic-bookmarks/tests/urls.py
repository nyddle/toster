try:
    from django.conf.urls.defaults import patterns, include
except ImportError:
    from django.conf.urls import patterns, include

urlpatterns = patterns('', (r'^bookmarks/', include('bookmarks.urls')))
