Getting started
===============

Requirements
~~~~~~~~~~~~

======  ======
Python  >= 2.5
Django  >= 1.3
======  ======

jQuery >= 1.4 is required if you want to take advantage of *AJAX* features 
described above and in :doc:`templatetags_api`.

``pip install mongoengine`` is needed if you want to use the MongoDB backend.

Installation
~~~~~~~~~~~~

The Mercurial repository of the application can be cloned with this command::

    hg clone https://bitbucket.org/frankban/django-generic-bookmarks

The ``bookmarks`` package, included in the distribution, should be
placed on the ``PYTHONPATH``.

Otherwise you can just ``pip install django-generic-bookmarks``.

Configuration
~~~~~~~~~~~~~

Add the request context processor in your *settings.py*, e.g.::
    
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    TEMPLATE_CONTEXT_PROCESSORS += (
         'django.core.context_processors.request',
    )
    
Add ``'bookmarks'`` to the ``INSTALLED_APPS`` in your *settings.py*.

The application, by default, uses Django models to save bookmarks in the
database. If you want to use MongoDB instead, just add in your *settings.py*::

    GENERIC_BOOKMARKS_BACKEND = 'bookmarks.backends.MongoBackend'
    GENERIC_BOOKMARKS_MONGODB = {"NAME": "bookmarks"}

See :doc:`customization` section in this documentation for other settings 
options and :doc:`backends_api` for a detailed description of provided
backends.

Add the bookmarks urls to your *urls.py*, e.g.::
    
    (r'^bookmarks/', include('bookmarks.urls')),
    
Time to create the needed database tables using *syncdb* management command::

    ./manage.py syncdb

Quickstart
~~~~~~~~~~

To allow a user to bookmark a Django model instance, the model must be
registered as *bookmarkable*, i.e. the system must know that instances
of that model can be bookmarked by users.

For example, if you have an *Article* model and you want users to add
articles to their favourites, you must register the model as bookmarkable,
e.g.::

    from bookmarks.handlers import library
    library.register(Article)

You can register models anywhere you like. However, you'll need to make sure 
that the module it's in gets imported early on so that the model gets 
registered before any bookmark is saved by the user.
This makes your app's *models.py* a good place to put the above code.

Under the hood you have registered the *Article* model with a default 
bookmark handler. Handlers are Python classes encapsulating bookmarking options 
for a given model, while *library* is a singleton registry that stores handlers.
For a detailed explanation see :doc:`handlers`.

Now it's time to let your users add an article to his favourites, and this 
is possible using one of the provided templatetags.
In the code below we assume that *article* is the *Article* model instance.

.. code-block:: html+django

    {% load bookmarks_tags %}

    {% bookmark_form for article %}

This code snippet just displays a form to add or remove the article
from user's favourites.

AJAX is also supported using jQuery, e.g.:

.. code-block:: html+django

    {% load bookmarks_tags %}

    <script src="path/to/jquery.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}bookmarks/bookmarks.js" type="text/javascript"></script>

    {% bookmark_form for article %}

It is possible to get the form as a template variable in the current context
instead of displaying it. This way we can customize the way the form is
presented, e.g.:

.. code-block:: html+django

    {% bookmark_form for article as form %} {# <-- note the 'as' argument #}

    <script src="path/to/jquery.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}bookmarks/bookmarks.js" type="text/javascript"></script>

    {% if form %}
        {% if user.is_authenticated %}
            <form action="{% url bookmarks_bookmark %}" method="post" accept-charset="UTF-8" class="bookmarks_form">
                {% csrf_token %}
                {{ form }}
                {% with form.bookmark_exists as exists %}
                    {# another hidden input is created to handle javascript submit event #}
                    <input class="bookmarks_toggle" type="submit" value="add"{% if exists %} style="display: none;"{% endif %}/>
                    <input class="bookmarks_toggle" type="submit" value="remove"{% if not exists %} style="display: none;"{% endif %}/>
                {% endwith %}                
                <span class="error" style="display: none;">Error during process</span>
            </form>
        {% else %}
            Handle anonymous users.
        {% endif %}
    {% endif %}


This application provides other templatetags (e.g.: for bookmarks retreival) 
and the ``bookmark_form`` has other useful options, explained in detail in
:doc:`templatetags_api`.

Note that the form template variable will be *None* if:
    - the user is not authenticated
    - the instance is not bookmarkable
    - the key is not allowed

What is a key? It is a way to define different kind of bookmarks.
For example, a user can add the article to his liked or to his disliked, and
so we need a key to tell the system what he is doing.
But this is an argument for the next section: :doc:`handlers`.
