try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module
from django.db import transaction
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
    
from bookmarks import settings, models, utils, exceptions

class BaseBackend(object):
    """
    Base bookmarks backend.
    
    Users may want to change *settings.GENERIC_BOOKMARKS_BACKEND*
    and customize the backend implementing all the methods defined here.
    """
    def get_model(self):
        """
        Must return the bookmark model (a Django model or anything you like).
        Instances of this model must have the following attributes:
        
            - user (who made the bookmark, a Django user instance)
            - key (the bookmark key, as string)
            - content_type (a Django content_type instance)
            - object_id (a pk for the bookmarked object)
            - content_object (the bookmarked object as a Django model instance)
            - created_at (the date when the bookmark is created)
        """
        raise NotImplementedError
        
    def add(self, user, instance, key):
        """
        Must create a bookmark for *instance* by *user* using *key*.
        Must return the created bookmark (as a *self.get_model()* instance).
        Must raise *exceptions.AlreadyExists* if the bookmark already exists.
        """
        raise NotImplementedError
        
    def remove(self, user, instance, key):
        """
        Must remove the bookmark identified by *user*, *instance* and *key*.
        Must return the removed bookmark (as a *self.get_model()* instance).
        Must raise *exceptions.DoesNotExist* if the bookmark does not exist.
        """
        raise NotImplementedError
        
    def remove_all_for(self, instance):
        """
        Must delete all the bookmarks related to given *instance*.
        """
        raise NotImplementedError
                
    def filter(self, **kwargs):
        """
        Must return all bookmarks corresponding to given *kwargs*.

        The *kwargs* keys can be:
            - user: Django user object or pk
            - instance: a Django model instance
            - content_type: a Django ContentType instance or pk
            - model: a Django model
            - key: the bookmark key to use
            - reversed: reverse the order of results

        The bookmarks must be an iterable (like a Django queryset) of
        *self.get_model()* instances.

        The bookmarks must be ordered by creation date (*created_at*):
        if *reversed* is True the order must be descending.
        """
        raise NotImplementedError

    def get(self, user, instance, key):
        """
        Must return a bookmark added by *user* for *instance* using *key*.
        Must raise *exceptions.DoesNotExist* if the bookmark does not exist.
        """
        raise NotImplementedError
        
    def exists(self, user, instance, key):
        """
        Must return True if a bookmark given by *user* for *instance*
        using *key* exists, False otherwise.
        """
        raise NotImplementedError
        

class ModelBackend(BaseBackend):
    """
    Bookmarks backend based on Django models.

    This is used by default if no other backend is specified.
    """
    def get_model(self):
        return models.Bookmark
    
    @transaction.commit_on_success  
    def add(self, user, instance, key):
        return self.get_model().objects.add(user, instance, key)
    
    @transaction.commit_on_success
    def remove(self, user, instance, key):
        return self.get_model().objects.remove(user, instance, key)
    
    @transaction.commit_on_success
    def remove_all_for(self, instance):
        self.get_model().objects.remove_all_for(instance)
    
    def filter(self, **kwargs):
        """
        The *kwargs* can be:
            - user: Django user object or pk
            - instance: a Django model instance
            - content_type: a Django ContentType instance or pk
            - model: a Django model
            - key: the bookmark key to use
            - reversed: reverse the order of results
        """
        order = '-created_at' if kwargs.pop('reversed', False) else 'created_at'
        if 'instance' in kwargs:
            instance = kwargs.pop('instance')
            kwargs.update({
                'content_type': utils.get_content_type_for_model(instance),
                'object_id': instance.pk,
            })
        elif 'model' in kwargs:
            model = kwargs.pop('model')
            kwargs['content_type'] = utils.get_content_type_for_model(model)
        if 'user' in kwargs:
            queryset = self.get_model().objects.filter_with_contents(**kwargs)
        else:
            queryset = self.get_model().objects.filter(**kwargs)
        return queryset.order_by(order)
                
    def get(self, user, instance, key):
        bookmark = self.get_model().objects.get_for(instance, key, user=user)
        if bookmark is None:
            raise exceptions.DoesNotExist
        return bookmark
        
    def exists(self, user, instance, key):
        return self.filter(instance=instance, user=user, key=key).exists()


class MongoBackend(BaseBackend):
    """
    Bookmarks backend based on MongoDB.
    """
    def __init__(self):
        # establishing mongodb connection
        import mongoengine
        self.ConnectionError = mongoengine.connection.ConnectionError
        name = settings.MONGODB["NAME"]
        username = settings.MONGODB.get("USERNAME")
        password = settings.MONGODB.get("PASSWORD")
        parameters = settings.MONGODB.get("PARAMETERS", {})
        try:
            self.db = mongoengine.connect(name, username, password, **parameters)
        except mongoengine.connection.ConnectionError:
            raise exceptions.MongodbConnectionError
        self._model = None

    def _get_content_type_id(self, instance):
        return utils.get_content_type_for_model(instance).id
    
    def _create_model(self):
        import datetime
        from mongoengine import Document, IntField, StringField, DateTimeField
        
        class Bookmark(Document):
            content_type_id = IntField(required=True, min_value=1)
            object_id = IntField(required=True, min_value=1)
            
            key = StringField(required=True, max_length=16)
            
            user_id = IntField(required=True, min_value=1, 
                unique_with=['content_type_id', 'object_id', 'key'])
            
            created_at = DateTimeField(required=True, 
                default=datetime.datetime.now)

            meta = {'indexes': ['user_id', ('content_type_id', 'object_id')]}

            def __unicode__(self):
                return 'Bookmark for %s by %s' % (self.content_object, 
                    self.user)

            def __eq__(self, other):
                return self.id == other.id

            @property
            def user(self):
                return User.objects.get(pk=self.user_id)
            
            @property
            def content_object(self):
                ct = ContentType.objects.get_for_id(self.content_type_id)
                return ct.get_object_for_this_type(pk=self.object_id)
        
        return Bookmark
    
    def get_model(self):
        if self._model is None:
            self._model = self._create_model()
        return self._model

    def add(self, user, instance, key):
        import mongoengine
        model = self.get_model()
        bookmark = model(
            content_type_id=self._get_content_type_id(instance),
            object_id=instance.pk,
            key=key,
            user_id=user.pk
        )
        try:
            bookmark.save()
        except mongoengine.OperationError:
            raise exceptions.AlreadyExists
        return bookmark
        
    def remove(self, user, instance, key):
        bookmark = self.get(user, instance, key)
        bookmark.delete()
        return bookmark
        
    def remove_all_for(self, instance):
        model = self.get_model()
        model.objects.filter(
            content_type_id=self._get_content_type_id(instance),
            object_id=instance.pk,
        ).delete()
                
    def filter(self, **kwargs):
        """
        The *kwargs* can be:
            - user: Django user object or pk
            - instance: a Django model instance
            - content_type: a Django ContentType instance or pk
            - model: a Django model
            - key: the bookmark key to use
            - reversed: reverse the order of results
        """
        order = '-created_at' if kwargs.pop('reversed', False) else 'created_at'
        if 'instance' in kwargs:
            instance = kwargs.pop('instance')
            kwargs.update({
                'content_type_id': self._get_content_type_id(instance),
                'object_id': instance.pk,
            })
        elif 'model' in kwargs:
            model = kwargs.pop('model')
            kwargs['content_type'] = self._get_content_type_id(model)
        return self.get_model().objects.filter(**kwargs).order_by(order)
    
    def get(self, user, instance, key):
        model = self.get_model()
        try:
            return model.objects.get(
                content_type_id=self._get_content_type_id(instance),
                object_id=instance.pk,
                key=key,
                user_id=user.pk
            )
        except model.DoesNotExist:
            raise exceptions.DoesNotExist
        
    def exists(self, user, instance, key):
        try:
            self.get(user, instance, key)
        except exceptions.DoesNotExist:
            return False
        return True
        
        
def get_backend():
    if settings.BACKEND is None:
        return ModelBackend()
    i = settings.BACKEND.rfind('.')
    module, attr = settings.BACKEND[:i], settings.BACKEND[i+1:]
    try:
        mod = import_module(module)
    except ImportError as err:
        message = 'Error loading bookmarks backend %s: "%s"'
        raise ImproperlyConfigured(message % (module, err))
    try:
        backend_class = getattr(mod, attr)
    except AttributeError:
        message = 'Module "%s" does not define a bookmarks backend named "%s"'
        raise ImproperlyConfigured(message % (module, attr))
    return backend_class()
