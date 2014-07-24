Backends reference
==================

.. py:module:: bookmarks.backends

The function of backends is to handle bookmarks retreival and save.
They take care of things like adding or removing a bookmark, and getting 
all bookmarks based on some filters.

Writing your own backend
~~~~~~~~~~~~~~~~~~~~~~~~

The application ships with a Django model backend and a MongoDB backend,
but you can add your own defining a class with the interface below and 
pointing ``settings.GENERIC_BOOKMARKS_BACKEND`` to the new customized one.

.. py:class:: BaseBackend

    Base bookmarks backend.
    
    Users may want to change ``settings.GENERIC_BOOKMARKS_BACKEND``
    and customize the backend implementing all the methods defined here.

    .. py:method:: get_model(self)

        Must return the bookmark model (a Django model or anything you like).
        Instances of this model must have the following attributes:
        
            - user (who made the bookmark, a Django user instance)
            - key (the bookmark key, as string)
            - content_type (a Django content_type instance)
            - object_id (a pk for the bookmarked object)
            - content_object (the bookmarked object as a Django model instance)
            - created_at (the date when the bookmark is created)

    .. py:method:: add(self, user, instance, key)

        Must create a bookmark for *instance* by *user* using *key*.
        Must return the created bookmark (as a *self.get_model()* instance).
        Must raise *exceptions.AlreadyExists* if the bookmark already exists.

    .. py:method:: remove(self, user, instance, key)

        Must remove the bookmark identified by *user*, *instance* and *key*.
        Must return the removed bookmark (as a *self.get_model()* instance).
        Must raise *exceptions.DoesNotExist* if the bookmark does not exist.

    .. py:method:: remove_all_for(self, instance)

        Must delete all the bookmarks related to given *instance*.

    .. py:method:: filter(self, **kwargs)

        Must return all bookmarks corresponding to given *kwargs*.

        The *kwargs* keys can be:
            - user: Django user object or pk
            - instance: a Django model instance
            - content_type: a Django ContentType instance or pk
            - model: a Django model
            - key: the bookmark key to use
            - reversed: reverse the order of results

        The bookmarks must be an iterable (like a Django queryset) of
        *self.get_model()* instances.

        The bookmarks must be ordered by creation date (*created_at*):
        if *reversed* is True the order must be descending.

    .. py:method:: get(self, user, instance, key)

        Must return a bookmark added by *user* for *instance* using *key*.
        Must raise *exceptions.DoesNotExist* if the bookmark does not exist.

    .. py:method:: exists(self, user, instance, key)

        Must return True if a bookmark given by *user* for *instance*
        using *key* exists, False otherwise.


Django
~~~~~~

The default backend used if ``settings.GENERIC_BOOKMARKS_BACKEND`` is *None*
is ``ModelBackend``, that uses Django models to store bookmarks.

.. py:class:: ModelBackend(BaseBackend)

    Bookmarks backend based on Django models.

    This is used by default if no other backend is specified.


MongoDB
~~~~~~~

In order to use the MongoDB backend you must change your settings file like::

    GENERIC_BOOKMARKS_BACKEND = 'bookmarks.backends.MongoBackend'
    GENERIC_BOOKMARKS_MONGODB = {"NAME": "bookmarks"}

and then install MongoEngine::

    pip install mongoengine

See :doc:`customization` for a more complete explanation of MongoDB settings.

.. py:class:: MongoBackend(BaseBackend)

    Bookmarks backend based on MongoDB.

