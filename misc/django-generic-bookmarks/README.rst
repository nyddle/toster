Django Generic Bookmarks
========================

This application provides bookmarks management functionality to 
a Django project.

For instance, using bookmarks, users can store their favourite
contents, or items they follow, or topics they like or dislike.

A bookmark connects users to Django contents in a generic way, without
modifying existing models tables, and *django-generic-bookmarks* exposes
a simple API to handle them, yet allowing the management of bookmarks
in complex scenarios too.

The bookmarks can be stored using different backends. 
The default one uses Django models to store user's preferences in the database,
but it is possible to write customized backends, and the application, 
out of the box, includes also a MongoDB backend.

The source code for this app is hosted on 
https://bitbucket.org/frankban/django-generic-bookmarks

**Documentation** is avaliable 
`online <http://django-generic-bookmarks.readthedocs.org/>`_ 
and in the docs directory of the project.
