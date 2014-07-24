try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url

urlpatterns = patterns('bookmarks.views',
    url(r'^bookmark/$', 'bookmark', name='bookmarks_bookmark'),
    url(r'^ajax_form/$', 'ajax_form', name='bookmarks_ajax_form'),
)