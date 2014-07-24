class BookmarksError(Exception):
    """
    Base exception class for generic bookmarks app.
    """
    pass

        
class AlreadyHandled(BookmarksError):
    """
    Raised when a model which is already registered for bookmarks is
    attempting to be registered again.
    """
    pass


class NotHandled(BookmarksError):
    """
    Raised when a model which is not registered for bookmarks is
    attempting to be unregistered.
    """
    pass
    

class AlreadyExists(BookmarksError):
    """
    The bookmark you are trying to create already exists.
    """
    

class DoesNotExist(BookmarksError):
    """
    The bookmark you are trying to remove does not exists.
    """


class MongodbConnectionError(BookmarksError):
    """
    Cannot connect to mongodb.
    """