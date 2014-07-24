Usage and examples
==================

As seen previously in :doc:`handlers`, we can customize the bookmark process
creating and registering bookmarks handlers.

In this section we will deal with some real-world examples of usage of 
Django Generic Bookmarks.


Simple bookmarks
~~~~~~~~~~~~~~~~

As seen in :doc:`getting_started`, adding bookmarks functionality to a
Django project is straightforward.

It is only needed to register bookmarkable models (*Article* in our example)::

    from bookmarks.handlers import library
    library.register(Article)

and then to display the form using a templatetag, having *article* as
an *Article* model instance:

.. code-block:: html+django

    {% load bookmarks_tags %}

    {% bookmark_form for article %}


Multiple types of bookmarks
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assume we want users to follow site contents and/or to share them.
This means that we want two types of bookmark for a single model instance:
let' say ``followed`` and ``shared``.

First, we have to register a model informing the system that the two keys
above are allowed::

    from bookmarks.handlers import library, Handler
    ratings.register(MyModel, Handler, allowed_keys=['followed', 'shared'])

And then, in the template, we get one bookmark form for each key:

.. code-block:: html+django

    {# follow/unfollow #}

    {% bookmark_form for article using 'followed' as follow_form %} {# <-- note the 'using' argument #}

    {% if follow_form %}
        {% if user.is_authenticated %}
            <form action="{% url bookmarks_bookmark %}" method="post" accept-charset="UTF-8" class="bookmarks_form">
                {% csrf_token %}
                {{ follow_form }}
                {% with follow_form.bookmark_exists as exists %}
                    {# another hidden input is created to handle javascript submit event #}
                    <input class="bookmarks_toggle" type="submit" value="follow"{% if exists %} style="display: none;"{% endif %}/>
                    <input class="bookmarks_toggle" type="submit" value="stop following"{% if not exists %} style="display: none;"{% endif %}/>
                {% endwith %}                
                <span class="error" style="display: none;">Errors during process</span>
            </form>
        {% else %}
            Handle anonymous users.
        {% endif %}
    {% endif %}

    {# share/unshare #}

    {% bookmark_form for article using 'shared' as share_form %} {# <-- note the 'using' argument #}

    {% if share_form %}
        {% if user.is_authenticated %}
            <form action="{% url bookmarks_bookmark %}" method="post" accept-charset="UTF-8" class="bookmarks_form">
                {% csrf_token %}
                {{ share_form }}
                {% with share_form.bookmark_exists as exists %}
                    {# another hidden input is created to handle javascript submit event #}
                    <input class="bookmarks_toggle" type="submit" value="share"{% if exists %} style="display: none;"{% endif %}/>
                    <input class="bookmarks_toggle" type="submit" value="unshare"{% if not exists %} style="display: none;"{% endif %}/>
                {% endwith %}                
                <span class="error" style="display: none;">Errors during process</span>
            </form>
        {% else %}
            Handle anonymous users.
        {% endif %}
    {% endif %}

Note that we are using two submit inputs for each form, and all of them have 
*bookmarks_toggle* html class: this is not required, but it makes easier for 
a Javascript to show and hide them based on AJAX request, as described below.

See :doc:`forms_api` to know more about forms, and :doc:`templatetags_api`
for further explanation about provided templatetags.


Conditional bookmarks
~~~~~~~~~~~~~~~~~~~~~

Assume we want the system to automatically assign a key to bookmarks based on 
some conditions.

For example, we want users to express an interest for not yet released
films, or to like them when they finally are on theaters.

So we need to switch between two keys (let's say ``interests`` and ``likes``)
based on release status of the film::

    import datetime
    from bookmarks.handlers import library, Handler

    class FilmHandler(Handler):

        allowed_keys = ('interests', 'likes')

        def get_key(self, request, instance, key=None):
            if key is None:
                today = datetime.date.today()
                key = 'interests' if instance.release_date < today else 'likes' 
            return key

    library.register(Film, FilmHandler)

Nothing remains but to retreive the form in the template 
without specifying the key to use.


Add/remove bookmarks using links
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you may want to use links instead of submit inputs to let users
add or remove bookmarks.

This is achievable using a little bit of Javascript, and jQuery of course:

.. code-block:: html+django

    {% bookmark_form for article as form %} {# <-- note the 'using' argument #}

    {% if form %}
        {% if user.is_authenticated %}
            <form action="{% url bookmarks_bookmark %}" method="post" accept-charset="UTF-8" class="bookmarks_form">
                {% csrf_token %}
                {{ form }}
                {% with form.bookmark_exists as exists %}
                    <span class="bookmarks_toggle"{% if exists %} style="display:none"{% endif %}>
                        <a rel="nofollow" href="javascript:void(0)" onclick="$(this).closest('form').submit();">Follow</a>
                    </span>
                    <span class="bookmarks_toggle"{% if not exists %} style="display:none"{% endif %}>
                        <a rel="nofollow" href="javascript:void(0)" onclick="$(this).closest('form').submit()">Stop following</a>)
                    </span>
                {% endwith %}                
                <span class="error" style="display: none;">Errors during process</span>
            </form>
        {% else %}
            Handle anonymous users.
        {% endif %}
    {% endif %}

This is only an example of how to submit a form using the *onclick* event of
a link.


Using AJAX
~~~~~~~~~~

In all the examples seen above, the form is used with some tricks:

    - the form class is *bookmarks_form*
    - we use two elements to submit the form, one for adding and one
      for removing a bookmark, and one of them is deactivated (not displayed)
    - theese two elements have *bookmarks_toggle* html class
    - there is a hidden element with class *error*

They are really needed only if you want to use AJAX in the bookmark process
loading in the template jQuery and the provided *bookmarks.js*, e.g.:

.. code-block:: html+django

    {% bookmark_form for article as form %}

    <script src="path/to/jquery.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}bookmarks/bookmarks.js" type="text/javascript"></script>

    ...

The Javascript performs various operations:

    - POST data to the server using AJAX
    - toggle the elements having *bookmarks_toggle* html class
    - if errors occurs during process, show the element having *error* class
    - trigger the ``bookmarked`` event on the form, with data returned by 
      the server, e.g.:: 

        {
            'key': 'the_bookamrk_key',
            'bookmark_id': bookmark.id,
            'user_id': <the id of the bookmarker>,
            'created': <True if bookmark is created, False otherwise>,
        }


Performance and database denormalization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One goal of *Django Generic Bookmarks* is to provide a generic solution to 
connect model instances to users without the need to edit your (or third party) 
models.

Sometimes, however, you may want to denormalize data, for example
because you need to minimize queries for tables with a lot of 
records, or for backward compatibility with legacy code.

Assume you want to store the bookmarks count for your model instances.
For example, we want to store the number of users who liked an article.

This is easily achievable, again, customizing the handler, e.g.::
    
    from bookmarks.handlers import library, Handler

    class ArticleHandler(Handler):

        def post_save(self, request, bookmark, added):
            if bookmark.key == 'likes':
                count = self.backend.filter(key=bookmark.key).count()
                instance = bookmark.content_object
                instance.num_likes = count
                instance.save()

    library.register(Article, ArticleHandler)


Bookmarks and cache
~~~~~~~~~~~~~~~~~~~

See **ajax_bookmark_form** in :doc:`templatetags_api`.


Retreiving bookmarks
~~~~~~~~~~~~~~~~~~~~

The backend used to store and retreive bookmarks is always accessible
from the *library* registry.

While a complete description of backends can be found in :doc:`backends_api`,
here is a brief summary of the API::

    from bookmarks.handlers import library
    
    # get all bookmarks saved by a user
    bookmarks = library.backend.filter(user=user)

    # get all bookmarks of a specified instance and key
    bookmarks = library.backend.filter(instance=article, key='likes')

    # get all articles bookmarks
    bookmarks = library.backend.filter(model=Article)

    # add/remove bookmarks
    bookmark = library.backend.add(user, article, 'likes')
    bookmark = library.backend.remove(user, article, 'likes')

    # get a bookmark
    bookmark = library.backend.get(user, article, 'likes')

    # check for bookamrk existance
    exists = library.backend.exists(user, article, 'likes')

Note that backend is also present as an attribute of handlers, e.g.::

    from bookmarks.handlers import library
    handler = library.get_handler(Article)
    backend = handler.backend

It is easy to retreive bookmarks in templates using the **bookmark**
and **bookmarks** templatetags (see :doc:`templatetags_api`).


Annotating user's bookmarks
~~~~~~~~~~~~~~~~~~~~~~~~~~~

See **annotate_bookmarks** function in :doc:`models_api`.


Deleting model instances
~~~~~~~~~~~~~~~~~~~~~~~~

To preserve database integrity, when you delete a model instance 
all related bookmarks are contextually deleted too.
