Using handlers
==============

As seen in :doc:`getting_started`, a model instance can be bookmarked by users 
only if its model class is handled. Being handled, for a model, 
means it is registered with a bookmarks handler.

We have seen how to do that::

    from bookmarks.handlers import library
    library.register(MyModel)

The handler class is an optional argument of the ``library.register`` method,
and, if not provided, the default ``bookmarks.handlers.Handler`` is used.

The previous code can be written::

    from bookmarks.handlers import library, Handler
    ratings.register(MyModel, Handler)

For convenience, ``library.register`` can also accept a list 
of model classes in place of a single model; this allows easier 
registration of multiple models with the same handler class, e.g.::

    from bookmarks.handlers import library, Handler
    ratings.register([Article, BlogEntry], Handler)

You can register models anywhere you like. However, you'll need to make sure 
that the module it's in gets imported early on so that the model gets 
registered before any bookmark is saved by the user.
This makes your app's *models.py* a good place to put the above code.

Handlers are Python classes encapsulating bookmarking options for a given 
model, and theese options can be overridden while registering a model, e.g.::

    from bookmarks.handlers import library, Handler
    ratings.register(MyModel, Handler, 
        allowed_keys=['likes', 'dislikes'], form_class=MyCustomForm)

Three things are done in the code snippet above:
    - *MyModel* is registered as a bookmarkable model, i.e. users can
      save instances of that model as bookmarks.
    - Two types of bookmarks are allowed: *likes* and *dislikes*.
      This means that users can like or dislike *MyModel* instances
      (note that keys are just arbitrary strings)
    - *MyCustomForm* will be used to save bookmarks 
      (in place of the form provided by the application)

See :doc:`handlers_api` for a list of all available handlers options.

Later it is possible to retreive the handler instance used to 
manage bookmarks for a particular model or instance::

    from bookmarks.handlers import library
    # handler instance for article class
    handler = library.get_handler(article)
    # handler instance for MyModel
    handler = library.get_handler(MyModel)

Custom Handlers
~~~~~~~~~~~~~~~

There are situations where the built-in options are not sufficient.

What if, for instance, you want to use different forms for staff and normal
users?

As in Django own ``contrib.admin.ModelAdmin``, you can write subclasses of 
``bookmarks.handlers.Handler`` to override the methods which actually 
perform the bookmark process, and apply any logic you desire.

Here is an example meeting the needs described above::

    from bookmakrs.handlers import library, Handler
    
    class MyHandler(Handler):

        def get_form_class(self, request):
            """
            Return the form class that will be used to add or remove bookmarks.
            Default is *self.form_class*.
            """
            return StaffForm if request.user.is_staff else self.form_class
           
    library.register(MyModel, MyHandler)

Examples of handler customizations can be found in :doc:`usage_examples`.

Handlers API
~~~~~~~~~~~~

As seen in :doc:`getting_started`, you can let users add or remove 
bookmarks using a simple templatetag:

.. code-block:: html+django

    {% load bookmarks_tags %}

    {% bookmark_form for article %}

But what happens when the user clicks to add or remove a bookmark?

The handler is used to do the real work.

1. Key management
-----------------

Initially the handler is responsable of producing a valid bookmark *key*.

The key is an arbitrary string representing the type of bookmark we are saving.
For example, users can like an article or hate it, or maybe they want to be
notified on comments of that article. Theese are different types of bookmarks
and can be expressed using different keys 
(e.g.: ``likes``, ``hates``, ``comments``).

The two methods called to handle keys are:

.. py:method:: get_key(self, request, instance, key=None)

    Return the bookmark key to be used to save the bookmark of *instance*.
    
    Subclasses can return different keys based on the *request*, on
    the given target object *instance* or the optional *key*
    that can be provided for example by the templatetags.

    Here is an example of a templatetag providing a key:

    .. code-block:: html+django

        {% load bookmarks_tags %}
        {% bookmark_form for article using 'favourite' %}
    
    For example, if you want a different key to be used if the user is
    staff, you can override this method in this way::
    
        def get_key(self, request, instance, key=None):
            return 'staff' if request.user.is_superuser else 'normal'

    If you do not customize things, this method returns the given *key* 
    (if not *None*) or a default key ``main``.

.. py:method:: allow_key(self, request, instance, key)

    This method is called when the user tries to bookmark an object 
    using the given bookmark *key* (e.g. when the bookmark view is 
    called with POST data).
    
    The bookmarking process continues only if this method returns True
    (i.e. a valid key is passed).
    
    For example, if you want two different bookmarks for each 
    target object, you can use two forms (each providing a different 
    key, say 'main' and 'other') and then allow those keys::
    
        def allow_key(self, request, instance, key):
            return key in ('main', 'other')

    By default this method allows keys listed in *self.allowed_keys*.

See :doc:`usage_examples` for a deeper explanation of how to handle keys.

2. Bookmark saving
------------------

Five handlers methods are involved in bookmarks saving:

.. py:method:: get_form(self, request, **kwargs)

    that returns the form that actually adds or remove a bookmark,
    and that calls...

.. py:method:: get_form_class(self, request)
    
    to get the form class used (usually is *Handler.form_class* 
    that by default points to *bookmarks.forms.BookmarkForm*).

.. py:method:: pre_save(self, request, form)

    Called just before the bookmark is added or removed, this method 
    takes the *request* and the *form* instance.
    
    Subclasses can use this method to check if the bookmark can be saved 
    or deleted, and, if necessary, block the bookmarking process 
    returning False.
    
    This method is called by a *signals.bookmark_pre_save* receiver 
    always attached to the handler by the registry.

    It's up to the developer if override this method or just connect
    another listener to the signal: the bookmarking process is killed 
    if just one receiver returns False.

.. py:method:: save(self, request, form)

    Save the bookmark to the database.
    Return the saved bookmark. 

.. py:method:: post_save(self, request, bookmark, added)

    Called just after a bookmark is added or removed.

    The given arguments are the current *request*, the just added
    or deleted *bookmark* and the boolean *added* 
    (True if the bookmark was added).
    
    This method is called by a *signals.bookmark_post_save* receiver
    always attached to the handler by the registry.

    It's up to the developer if override this method or just connect
    another listener to the signal.
    
    By default, this method does noting.

3. HTTP Response
----------------

Finally, the reponse to the client is managed by

.. py:method:: response(self, request, bookmark, created)

    that, by default, calls...

.. py:method:: ajax_response(self, request, bookmark, created)

    Called if the request is ajax.
    Return a JSON reponse containing::
    
        {
            'key': 'the_bookamrk_key',
            'bookmark_id': bookmark.id,
            'user_id': <the id of the bookmarker>,
            'created': <True if bookmark is created, False otherwise>,
        }

or 

.. py:method:: normal_response(self, request, bookmark, created)

    Called by *self.response* when the request is not ajax.
    Return a redirect response.

-----

While the complete handlers API is described in :doc:`handlers_api`, maybe
now it's time to read :doc:`usage_examples`.
