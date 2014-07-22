Templatetags reference
======================

In order to use the following templatetags you must 
``{% load bookmarks_tags %}`` in your template.

.. py:module:: bookmarks.templatetags.bookmarks_tags

bookmark_form
~~~~~~~~~~~~~

.. py:function:: bookmark_form(parser, token)

    Return, as html or as a template variable, a Django form to add or remove 
    a bookmark for the given instance and key, and for current user.

    Usage:
    
    .. code-block:: html+django

        {% bookmark_form for *instance* [using *key*] [as *varname*] %}
    
    The key can be given hardcoded (surrounded by quotes) 
    or as a template variable.
    Note that if the key is not given, it will be generated using 
    the handler's *get_key* method, that, if not overridden, returns
    the default key. 

    If the *varname* is used then it will be a context variable 
    containing the form.
    Otherwise the form is rendered using the first template found in the order
    that follows::

        bookmarks/[app_name]/[model_name]/[key]/form.html
        bookmarks/[app_name]/[model_name]/form.html
        bookmarks/[app_name]/[key]/form.html
        bookmarks/[app_name]/form.html
        bookmarks/[key]/form.html
        bookmarks/form.html
    
    The *app_name* and *model_name* refer to the instance given as
    argument to this templatetag.

    Example:

    .. code-block:: html+django

        {% bookmark_form for myinstance using 'mykey' as form %}

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

    The template variable (or the html) will be None if:
        - the user is not authenticated
        - the instance is not bookmarkable
        - the key is not allowed

    AJAX is also supported using jQuery, e.g.:

    .. code-block:: html+django

        {% load bookmarks_tags %}

        <script src="path/to/jquery.js" type="text/javascript"></script>
        <script src="{{ STATIC_URL }}bookmarks/bookmarks.js" type="text/javascript"></script>

        {% bookmark_form for article %}


ajax_bookmark_form
~~~~~~~~~~~~~~~~~~

.. py:function:: ajax_bookmark_form(parser, token)

    Use this just like the *bookmark_form* templatetag.
    The only difference here is that it always render a form template
    (so you can't use the *as varname* part), and the form template
    is rendered using an AJAX request.

    This is useful for example when you want to show add/remove
    bookamrk interaction for authenticated users even in a cached template.

    You need to load jQuery before using this templatetag.


bookmark
~~~~~~~~

.. py:function:: bookmark(parser, token)

    Return as a template variable a bookmark object for the given instance
    and key, and for current user.

    Usage:
    
    .. code-block:: html+django

        {% bookmark for *instance* [using *key*] as *varname* %}
    
    The key can be given hardcoded (surrounded by quotes) 
    or as a template variable.
    Note that if the key is not given, it will be generated using 
    the handler's *get_key* method, that, if not overridden, returns
    the default key. 

    The template variable will be None if:
        - the user is not authenticated
        - the instance is not bookmarkable
        - the bookmark does not exist


bookmarks
~~~~~~~~~

.. py:function:: bookmarks(parser, token)

    Return as a template variable all bookmarks, with possibility to filter 
    them by user, or to take only bookmarks of a particular model and
    using a specified key. It is also possible to reverse the order 
    of bookmarks (by default they are ordered by date).

    Usage:
    
    .. code-block:: html+django

        {% bookmarks [of *model*] [by *user*] [using *key*] [reversed] as *varname* %}

    Examples:

    .. code-block:: html+django

        {# get all bookmarks saved by myuser #}
        {% bookmarks by myuser as myuser_bookmarks %}

        {# get all bookmarks for myinstance using mykey #}
        {% bookmarks of myinstance using *mykey* as bookmarks %}

        {# getting all bookmarks for model 'myapp.mymodel' in reverse order #}
        {% bookmarks of 'myapp.mymodel' reversed as varname %}

    Note that the args *model* can be:

        - a model name as string (e.g.: 'myapp.mymodel')
        - a model instance

    The key can be given hardcoded (surrounded by quotes) 
    or as a template variable.
