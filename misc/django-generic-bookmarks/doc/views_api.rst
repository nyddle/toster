Class based views
=================

The application provides two generic class based views 
(only available if you are using Django >= 1.3).

.. py:module:: bookmarks.views.generic

BookmarksForView
~~~~~~~~~~~~~~~~

.. py:class:: BookmarksForView(BookmarksMixin, DetailView)

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

    .. py:attribute:: context_bookmarks_name

        The name of context variable containing bookmarks.
        Default is *'bookmarks'*.

    .. py:attribute:: key

        The bookmarks key to use for retreiving bookmarks.
        Default is *None*.

    .. py:attribute:: reversed_order

        If True, bookmarks are ordered by creation date descending.
        Default is True.

    .. py:method:: get_context_bookmarks_name(self, obj)

        Get the variable name to use for the bookmarks.

    .. py:method:: get_key(self, obj)

        Get the key to use to retreive bookmarks.
        If the key is None, use all keys.
    
    .. py:method:: order_is_reversed(self, obj)

        Return True to sort bookmarks by creation date descending.
    
    .. py:method:: get_bookmarks(self, obj, key, is_reversed)

        Return a queryset of bookmarks of *obj*.


BookmarksByView
~~~~~~~~~~~~~~~
        
.. py:class:: BookmarksByView(BookmarksMixin, DetailView)

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

    .. py:attribute:: context_bookmarks_name

        The name of context variable containing bookmarks.
        Default is *'bookmarks'*.

    .. py:attribute:: key

        The bookmarks key to use for retreiving bookmarks.
        Default is *None*.

    .. py:attribute:: reversed_order

        If True, bookmarks are ordered by creation date descending.
        Default is True.

    .. py:method:: get_context_bookmarks_name(self, obj)

        Get the variable name to use for the bookmarks.

    .. py:method:: get_key(self, obj)

        Get the key to use to retreive bookmarks.
        If the key is None, use all keys.
    
    .. py:method:: order_is_reversed(self, obj)

        Return True to sort bookmarks by creation date descending.
    
    .. py:method:: get_bookmarks(self, obj, key, is_reversed)

        Return a queryset of bookmarks saved by *obj* user.
