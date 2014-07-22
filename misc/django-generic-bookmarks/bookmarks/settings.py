from django.conf import settings

# default bookmark model (if None, *bookmarks.backends.ModelBackend* is used)
# to use MongoDB backend you can just write::
# GENERIC_BOOKMARKS_BACKEND = 'bookmarks.backends.MongoBackend'
BACKEND = getattr(settings, 'GENERIC_BOOKMARKS_BACKEND', None)

# default key to use for bookmarks when there is only one bookmark-per-content
DEFAULT_KEY = getattr(settings, 'GENERIC_BOOKMARKS_DEFAULT_KEY', 'main')

# querystring key that can contain the url of the redirection 
# performed after adding or removing bookmarks
NEXT_QUERYSTRING_KEY = getattr(settings, 
    'GENERIC_BOOKMARKS_NEXT_QUERYSTRING_KEY', 'next')

# set to False if you want to globally disable bookmarks deletion
CAN_REMOVE_BOOKMARKS = getattr(settings, 
    'GENERIC_BOOKMARKS_CAN_REMOVE_BOOKMARKS', True)

# mongodb backend connection parameters
# if the instance of MongoDB is executed in localhost without authentication 
# you can just write::
# GENERIC_BOOKMARKS_MONGODB = {"NAME": "bookmarks"}
MONGODB = getattr(settings, "GENERIC_BOOKMARKS_MONGODB", {
    'NAME': '', 
    'USERNAME': '',
    'PASSWORD': '',
    'PARAMETERS': {}, 
})
