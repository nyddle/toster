"""
Class based generic views.
These views are only available if you are using Django >= 1.3.
"""
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView

from bookmarks.handlers import library

class BookmarksMixin(object):
    """
    Mixin for bookmarks class based views.
    Views subclassing this class must implement the *get_bookmarks* method.

    .. py:attribute:: context_bookmarks_name

        The name of context variable containing bookmarks.
        Default is *'bookmarks'*.

    .. py:attribute:: key

        The bookmarks key to use for retreiving bookmarks.
        Default is *None*.

    .. py:attribute:: reversed_order

        If True, bookmarks are ordered by creation date descending.
        Default is True.
    """
    context_bookmarks_name = 'bookmarks'
    template_name_suffix = '_bookmarks'
    key = None
    reversed_order = True

    def get_context_bookmarks_name(self, obj):
        """
        Get the variable name to use for the bookmarks.
        """
        return self.context_bookmarks_name

    def get_key(self, obj):
        """
        Get the key to use to retreive bookmarks.
        If the key is None, use all keys.
        """
        return self.key

    def order_is_reversed(self, obj):
        """
        Return True to sort bookmarks by creation date descending.
        """
        return self.reversed_order

    def get_context_data(self, **kwargs):
        context = super(BookmarksMixin, self).get_context_data(**kwargs)
        context_bookmarks_name = self.get_context_bookmarks_name(self.object)
        key = self.get_key(self.object)
        is_reversed = self.order_is_reversed(self.object)
        bookmarks = self.get_bookmarks(self.object, key, is_reversed)
        context[context_bookmarks_name] = bookmarks
        return context

    def get_bookmarks(self, obj, key, is_reversed):
        """
        Must return a bookmark queryset.
        """
        raise NotImplementedError


class BookmarksForView(BookmarksMixin, DetailView):
    """
    Can be used to retreive and display a list of bookmarks of a given object.

    This class based view accepts all the parameters that can be passed
    to *django.views.generic.detail.DetailView*.

    For example, you can add in your *urls.py* a view displaying all
    bookmarks of a single active article::
    
        from bookmarks.views.generic import BookmarksForView
        
        urlpatterns = patterns('',
            url(r'^(?P<slug>[-\w]+)/bookmarks/$', BookmarksForView.as_view(
                queryset=Article.objects.filter(is_active=True)),
                name="article_bookmarks"),
        )

    You can also manage bookmarks order (default is by date descending) and
    bookmarks keys, in order to retreive only bookmarks for a given key, e.g.::

        from bookmarks.views.generic import BookmarksForView
        
        urlpatterns = patterns('',
            url(r'^(?P<slug>[-\w]+)/bookmarks/$', BookmarksForView.as_view(
                model=Article, key='mykey', reversed_order=False),
                name="article_bookmarks"),
        )
    
    Two context variables will be present in the template:
        - *object*: the bookmarked article
        - *bookmarks*: all the bookmarks of that article
        
    The default template suffix is ``'_bookmarks'``, and so the template
    used in our example is ``article_bookmarks.html``.


    """  
    def get_bookmarks(self, obj, key, is_reversed):
        """
        Return a queryset of bookmarks of *obj*.
        """
        lookups = {'instance': obj, 'reversed': is_reversed}
        if key is not None:
            lookups['key'] = key
        return library.backend.filter(**lookups)


class BookmarksByView(BookmarksMixin, DetailView):
    """
    Can be used to retreive and display a list of bookmarks saved by a  
    given user.

    This class based view accepts all the parameters that can be passed
    to *django.views.generic.detail.DetailView*, with an exception:
    it is not mandatory to specify the model or queryset used to
    retreive the user (*django.contrib.auth.models.User* model is used
    by default).

    For example, you can add in your *urls.py* a view displaying all
    bookmarks by a single active user::
    
        from bookmarks.views.generic import BookmarksByView
        
        urlpatterns = patterns('',
            url(r'^(?P<pk>\d+)/bookmarks/$', BookmarksByView.as_view(
                queryset=User.objects.filter(is_active=True)),
                name="user_bookmarks"),
        )
    
    You can also manage bookmarks order (default is by date descending) and
    bookmarks keys, in order to retreive only bookmarks for a given key, e.g.::

        from bookmarks.views.generic import BookmarksByView
        
        urlpatterns = patterns('',
            url(r'^(?P<pk>\d+)/bookmarks/$', BookmarksByView.as_view(
                key='mykey', reversed_order=False),
                name="user_bookmarks"),
        )

    Two context variables will be present in the template:
        - *object*: the user
        - *bookmarks*: all the bookmarks saved by that user
        
    The default template suffix is ``'_bookmarks'``, and so the template
    used in our example is ``user_bookmarks.html``.
    """
    model = User

    def get_bookmarks(self, obj, key, is_reversed):
        """
        Return a queryset of bookmarks saved by *obj* user.
        """
        lookups = {'user': obj, 'reversed': is_reversed}
        if key is not None:
            lookups['key'] = key
        return library.backend.filter(**lookups)
