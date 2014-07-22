Handlers reference
==================

.. py:module:: bookmarks.handlers

Default handler
~~~~~~~~~~~~~~~

.. py:class:: Handler

    Encapsulates content bookmarking options for a given model.
    
    This class can be subclassed to specify different behaviour and options
    for bookmarks of a given model, but can also be used directly, just to
    handle default any model using default options. 
    
    The default handler uses the project's settings as options: this 
    way you can register not customized handlers and then modify
    their options just editing the settings file.
    
    Most common bookmarking needs can be handled by subclassing *Handler* 
    and changing the values of pre-defined attributes. 
    The full range of built-in options is as follows.
    
        
    .. py:attribute:: default_key
        
        default key to use for bookmarks when there is only one 
        bookmark-per-content (default: *'main'*)

    .. py:attribute:: allowed_keys
        
        the bookmark allowed keys 
        (default: *['main']*)
        
    .. py:attribute:: next_querystring_key
    
        querystring key that can contain the url of the redirection performed 
        after bookmarking (default: *'next'*)
    
    .. py:attribute:: can_remove_bookmarks 
    
        set to False if you want to globally disable bookmarks deletion
        (default: *True*)
    
    .. py:attribute:: form_class
    
        form class that will be used to handle bookmark's adding and removing
        (default: *bookmarks.forms.BookmarkForm*) 
        
    For situations where the built-in options listed above are not sufficient, 
    subclasses of *Handler* can also override the methods which 
    actually perform the bookmarking process, and apply any logic they desire.
    
    See the method's docstrings for a description of how each method is
    used during the bookmarking process.

    .. py:method:: get_key(self, request, instance, key=None)

        Return the bookmark key to be used to save the bookmark.
        
        Subclasses can return different keys based on the *request*, on
        the given target object *instance* or the optional *key*
        (that can be provided for example by the templatetags).
        
        For example, if you want a different key to be used if the user is
        staff, you can override this method in this way::
        
            def get_key(self, request, instance, key=None):
                return 'staff' if request.user.is_superuser else 'normal'

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

    .. py:method:: get_form_class(self, request)

        Return the form class that will be used to add or remove bookmarks.
        Default is *self.form_class*.

    .. py:method:: get_form(self, request, **kwargs)

        Return an instance of the form, using given *request*, the backend 
        currently used by the handler and all given *kwargs*.

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
        Must return the saved bookmark. 

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

    .. py:method:: ajax_response(self, request, bookmark, created)

        Called by *self.response* when the request is ajax.
        Return a JSON reponse containing::
        
            {
                'key': 'the_bookamrk_key',
                'bookmark_id': bookmark.id,
                'user_id': <the id of the bookmarker>,
                'created': <True if bookmark is created, False otherwise>,
            }

    .. py:method:: normal_response(self, request, bookmark, created)

        Called by *self.response* when the request is not ajax.
        Return a redirect response.

    .. py:method:: response(self, request, bookmark, created)

        Callback used by the bookmarking views, called when the user 
        successfully added or removed a bookmark. 

        Must return a Django http response (usually a redirect, or
        some json if the request is ajax).

        The real job is done in the *ajax_response* and *normal_response*
        methods above.

    .. py:method:: fail(self, request, errors)

        Callback used by the bookmarking views, called when bookmark form 
        did not validate. Must return a Django http response.

    .. py:method:: remove_all_for(self, sender, instance, **kwargs)

        The target object *instance* of the model *sender*, is being deleted,
        so we must delete all the bookmarks related to that instance.
        
        This receiver is usually connected by the bookmark registry, when 
        a handler is registered.


Library
~~~~~~~

.. py:class:: Registry

    Registry that stores the handlers for each content type bookmarks system.

    An instance of this class will maintain a list of one or more models 
    registered for being bookmarked, and their associated handler classes.

    To register a model, obtain an instance of *Registry* (this module exports 
    one as *library*), and call its *register* method, passing the model class 
    and a handler class (which should be a subclass of *Handler*). 
    Note that both of these should be the actual classes, not instances 
    of the classes.

    To cease bookmarks handling for a model, call the *unregister* method,
    passing the model class.

    For convenience, both *register* and *unregister* can also accept a list 
    of model classes in place of a single model; this allows easier 
    registration of multiple models with the same *Handler* class.

    .. py:method:: register(self, model_or_iterable, handler_class=None, **kwargs)

        Register a model or a list of models for bookmark handling, using a 
        particular *handler_class*, e.g.::
        
            from bookmarks.handlers import library, Handler
            # register one model
            library.register(Article, Handler)
            # register other two models
            library.register([Film, Series], Handler)
        
        If the handler class is not given, the default 
        *bookmarks.handlers.Handler* class will be used.
        
        If *kwargs* are present, they are used to override the handler
        class attributes (using instance attributes), e.g.::
            
            library.register(Article, Handler, 
                can_remove_bookmarks=False, form_class=MyForm)

        Raise *AlreadyHandled* if any of the models are already registered.
        """

    .. py:method:: unregister(self, model_or_iterable)

        Remove a model or a list of models from the list of models that will
        be handled.

        Raise *NotHandled* if any of the models are not currently registered.

    .. py:method:: get_handler(self, model_or_instance)

        Return the handler for given model or model instance.
        Return None if model is not registered.
