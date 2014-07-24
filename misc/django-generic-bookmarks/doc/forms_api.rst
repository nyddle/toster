Forms reference
===============

.. py:module:: bookmarks.forms

.. py:class:: BookmarkForm(forms.Form)

    Form class to handle bookmarks.
    
    The bookmark is identified by *model*, *object_id* and *key*.
    The bookmark is added or removed based on the his existance.
    
    You can customize the app giving a custom form class, following
    some rules:
        
        - the form must provide the following fields:

            - model -> a string representation of app label and model name
              of the bookmarked object (e.g.: 'auth.user')
            - object_id -> the bookmarked instance id
            - key -> the bookmark key

        - the form must define the following methods:

            - bookmark_exists(self):
              return True if the current user has that instance with that key 
              in his bookmarks

            - instance(self):
              return the current instance to bookmark or None if the
              form data (content_type_id and object_id) is invalid

            - save(self):
              add or remove a bookmark and return it

    .. py:method:: __init__(self, request, backend, *args, **kwargs)
        
        Takes the current *request*, the bookmark's *backend* and all 
        the normal Django form arguments.

    .. py:method:: clean(self)

        Check if an instance with current *model* and *object_id* actually 
        exists in the database, and validate only if the user is authenticated.

    .. py:method:: instance(self)

        Return the bookmarked instance or None if the form is not valid.

        This method validates the form.

    .. py:method:: bookmark_exists(self)

        Return True if *self.instance* is bookmarked by the current user
        with the current key.

        Raise ValueError if the form is not valid.

        This method validates the form.

    .. py:method:: save(self)

        Add or remove the bookmark and return it.

        You must call this method only after form validation.
