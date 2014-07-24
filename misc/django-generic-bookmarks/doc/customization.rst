Customization
=============

When you register an handler you can customize all the bookmark options, as
seen in :doc:`handlers`.

But it is also possible to register an handler without overriding options 
or methods, and that handler will work using pre-defined global settings.

This section describes the settings used to globally customize bookmark 
handlers, together with their default values.

----

``GENERIC_BOOKMARKS_BACKEND = None``

default bookmark model (if None, *bookmarks.backends.ModelBackend* is used)

to use MongoDB backend you can just write::

    GENERIC_BOOKMARKS_BACKEND = 'bookmarks.backends.MongoBackend'

----

``GENERIC_BOOKMARKS_DEFAULT_KEY = 'main'``

default key to use for bookmarks when there is only one bookmark-per-content

----

``GENERIC_BOOKMARKS_NEXT_QUERYSTRING_KEY = 'next'``

querystring key that can contain the url of the redirection 
performed after adding or removing bookmarks

----

``GENERIC_BOOKMARKS_CAN_REMOVE_BOOKMARKS = True``

set to False if you want to globally disable bookmarks deletion

----

``GENERIC_BOOKMARKS_MONGODB = {'NAME': '', 'USERNAME': '', 'PASSWORD': '', 'PARAMETERS': {}}``

mongodb backend connection parameters

if the instance of MongoDB is executed in localhost without authentication 
you can just write::

    GENERIC_BOOKMARKS_MONGODB = {"NAME": "bookmarks"}
