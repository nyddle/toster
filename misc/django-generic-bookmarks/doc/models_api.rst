Models reference
================

.. py:module:: bookmarks.models

Objects defined here are only used if you store bookmarks using
default Django model backend.

Base models
~~~~~~~~~~~

.. py:class:: Bookmark(models.Model)

    A user's bookmark for a content object.

    This is only used if the current backend stores bookmarks in the database
    using Django models.

    .. py:attribute:: content_type

        the bookmarked instance content type

    .. py:attribute:: object_id

        the bookmarked instance id

    .. py:attribute:: content_object
        
        the bookmarked instance

    .. py:attribute:: key

        the bookmark key

    .. py:attribute:: user

        the user who bookmarked the instance 
        (as a fk to *django.contrib.auth.models.User*)

    .. py:attribute:: created_at

        the bookmark creation datetime

    .. py:attribute:: objects

        the manager used is *bookmarks.managers.BookmarksManager* (see below)


In bulk selections
~~~~~~~~~~~~~~~~~~

.. py:function:: annotate_bookmarks(queryset_or_model, key, user, attr='is_bookmarked')

    Annotate *queryset_or_model* with bookmarks, in order to retreive from
    the database all bookmark values in bulk.
    
    The first argument *queryset_or_model* must be, of course, a queryset
    or a Django model object. The argument *key* is the bookmark key.
    
    The bookmarks are filtered using given *user*.
    
    A boolean is inserted in an attr named *attr* (default='is_bookmarked')
    of each object in the generated queryset.
    
    Usage example::
    
        for article in annotate_bookmarks(Article.objects.all(), 'favourite', 
            myuser, attr='has_a_bookmark'):
            if article.has_a_bookmark:
                print u"User %s likes article %s" (myuser, article)


Abstract models
~~~~~~~~~~~~~~~

.. py:class:: BookmarkedModel(models.Model)

    Mixin for bookmarkable models.

    Models subclassing this abstract model gain a *bookmarks* attribute
    allowing accessto the reverse generic relation 
    to the *bookmarks.models.Bookmark*.


Managers
~~~~~~~~

.. py:module:: bookmarks.managers

.. py:class:: BookmarksManager(models.Manager)

    Manager used by *Bookmark* model.

    .. py:method:: get_for(self, content_object, key, **kwargs)

        Return the instance related to *content_object* and matching *kwargs*. 
        Return None if a bookmark is not found.

    .. py:method:: filter_for(self, content_object_or_model, **kwargs)

        Return all the instances related to *content_object_or_model* and 
        matching *kwargs*. The argument *content_object_or_model* can be
        both a model instance or a model class.

    .. py:method:: filter_with_contents(self, **kwargs)

        Return all instances retreiving content objects in bulk in order
        to minimize db queries, e.g. to get all objects bookmarked by a user::
        
            for bookmark in Bookmark.objects.filter_with_contents(user=myuser):
                bookmark.content_object # this does not hit the db

    .. py:method:: add(self, user, content_object, key)

        Add a bookmark, given the user, the model instance and the key.
        
        Raise a *Bookmark.AlreadyExists* exception if that kind of 
        bookmark is present in the db.

    .. py:method:: remove(self, user, content_object, key)

        Remove a bookmark, given the user, the model instance and the key.
        
        Raise a *Bookmark.DoesNotExist* exception if that kind of 
        bookmark is not present in the db.

    .. py:method:: remove_all_for(self, content_object)
        
        Remove all bookmarks for the given model instance.
        
        The application uses this whenever a bookmarkable model instance
        is deleted, in order to mantain the integrity of the bookmarks table.
