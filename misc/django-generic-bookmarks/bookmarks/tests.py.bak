from django.utils import unittest

from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from django.template import Template, Context
from django.test import client

from bookmarks import settings, exceptions, backends, handlers, forms, views
from bookmarks.models import annotate_bookmarks

class RequestFactory(client.RequestFactory):
    def __init__(self, user=None, *args, **kwargs):
        super(RequestFactory, self).__init__(*args, **kwargs)
        self.user = user or AnonymousUser()

    def request(self, *args, **kwargs):
        wsgi_request = super(RequestFactory, self).request(*args, **kwargs)
        wsgi_request.user = self.user
        return wsgi_request


class BookmarkTestModel(models.Model):
    name = models.CharField(max_length=8)
    
    def __unicode__(self):
        return unicode(self.name)


class BookmarkTestMixin(object):
    """
    Mixin for tests.
    """
    def create_user(self, username):
        return User.objects.create(username=username)
    
    def create_instance(self, name):
        return BookmarkTestModel.objects.create(name=name)

    def get_user_instance_key(self, prefix=''):
        user = self.create_user('%suser' % prefix)
        instance = self.create_instance('%sinstance' % prefix)
        key = '%skey' % prefix
        return user, instance, key

    def check_bookmark(self, bookmark, user, instance, key):
        self.assertEqual(bookmark.user, user)
        self.assertEqual(bookmark.content_object, instance)
        self.assertEqual(bookmark.key, key)

    def get_request(self, user=None, url='/', **kwargs):
        return RequestFactory(user, **kwargs).get(url)

    def clean(self):
        BookmarkTestModel.objects.all().delete()
        User.objects.all().delete()


# BACKEND TESTS
    
class BaseBackendTest(BookmarkTestMixin):
    def test_add_bookmark(self):
        user, instance, key = self.get_user_instance_key('add')
        bookmark = self.backend.add(user, instance, key)
        self.check_bookmark(bookmark, user, instance, key)

    def test_add_same_bookmark(self):
        user, instance, key = self.get_user_instance_key('addsame')
        bookmark = self.backend.add(user, instance, key)
        self.assertRaises(exceptions.AlreadyExists, 
            self.backend.add, user, instance, key)

    def test_bookmark_exists(self):
        user, instance, key = self.get_user_instance_key('exists')
        self.assertFalse(self.backend.exists(user, instance, key))
        self.backend.add(user, instance, key)
        self.assertTrue(self.backend.exists(user, instance, key))

    def test_remove_bookmark(self):
        user, instance, key = self.get_user_instance_key('remove')
        self.backend.add(user, instance, key)
        self.backend.remove(user, instance, key)
        self.assertFalse(self.backend.exists(user, instance, key))

    def test_remove_missing_bookmark(self):
        user, instance, key = self.get_user_instance_key('missing')
        self.assertRaises(exceptions.DoesNotExist, 
            self.backend.remove, user, instance, key)

    def test_filter_bookmarks(self):
        user1 = self.create_user('user_filter_1')
        user2 = self.create_user('user_filter_2')
        instance1 = self.create_instance('instance_filter_1')
        instance2 = self.create_instance('instance_filter_2')
        key1, key2 = 'key_filter_1', 'key_filter_2'

        bookmark1 = self.backend.add(user1, instance1, key1)
        bookmark2 = self.backend.add(user2, instance1, key1)
        bookmark3 = self.backend.add(user1, instance2, key1)
        bookmark4 = self.backend.add(user1, instance2, key2)
        bookmark5 = self.backend.add(user2, instance1, key2)

        bookmarks_user1 = list(self.backend.filter(user=user1))
        bookmarks_user1_reversed = list(self.backend.filter(user=user1, 
            reversed=True))
        bookmarks_user2_key2 = list(self.backend.filter(user=user2, key=key2))
        bookmarks_instance1 = list(self.backend.filter(instance=instance1))
        bookmarks_instance1_reversed = list(self.backend.filter(
            instance=instance1, reversed=True))
        bookmarks_instance2_user1 = list(self.backend.filter(instance=instance2, 
            user=user1))
        bookmarks_instance1_user2_key1 = list(self.backend.filter(
            instance=instance1, user=user2, key=key1))
        bookmarks_instance1_user1_key2 = list(self.backend.filter(
            instance=instance1, user=user1, key=key2))
        bookmarks_model = list(self.backend.filter(model=BookmarkTestModel))
        
        self.assertEqual(bookmarks_user1, [bookmark1, bookmark3, bookmark4])
        self.assertEqual(bookmarks_user1_reversed, 
            [bookmark4, bookmark3, bookmark1])
        self.assertEqual(bookmarks_user2_key2, [bookmark5])
        self.assertEqual(bookmarks_instance1, [bookmark1, bookmark2, bookmark5])
        self.assertEqual(bookmarks_instance1_reversed, 
            [bookmark5, bookmark2, bookmark1])
        self.assertEqual(bookmarks_instance2_user1, [bookmark3, bookmark4])
        self.assertEqual(bookmarks_instance1_user2_key1, [bookmark2])
        self.assertEqual(bookmarks_instance1_user1_key2, [])
        self.assertEqual(len(bookmarks_model), 5)

    def test_get_bookmark(self):
        user1 = self.create_user('user_get_1')
        user2 = self.create_user('user_get_2')
        instance1 = self.create_instance('instance_get_1')
        instance2 = self.create_instance('instance_get_2')
        key = 'key_get'

        bookmark1 = self.backend.add(user1, instance1, key)
        bookmark2 = self.backend.add(user2, instance1, key)

        self.assertEqual(self.backend.get(user2, instance1, key), bookmark2)
        self.assertRaises(exceptions.DoesNotExist, 
            self.backend.get, user1, instance2, key)

    def test_remove_all_bookmarks_for_instance(self):
        user1 = self.create_user('user_remove_all_1')
        user2 = self.create_user('user_remove_all_2')
        instance1 = self.create_instance('instance_remove_all_1')
        instance2 = self.create_instance('instance_remove_all_2')
        key1, key2 = 'key_remove_all_1', 'key_remove_all_2'

        self.backend.add(user1, instance1, key1)
        self.backend.add(user2, instance1, key1)
        self.backend.add(user1, instance1, key2)
        remaining = self.backend.add(user1, instance2, key1)

        self.backend.remove_all_for(instance1)

        bookmarks_instance1 = list(self.backend.filter(instance=instance1))
        bookmarks_instance2 = list(self.backend.filter(instance=instance2))

        self.assertEqual(bookmarks_instance1, [])
        self.assertEqual(bookmarks_instance2, [remaining])

    def test_bookmark_model(self):
        user, instance, key = self.get_user_instance_key('model')
        self.backend.add(user, instance, key)
        bookmarks = list(self.backend.filter(user=user))
        self.assertTrue(isinstance(bookmarks[0], self.backend.get_model()))

    
class DefaultBackendTestCase(unittest.TestCase, BaseBackendTest):
    def setUp(self):
        self.backend = backends.ModelBackend()

    def tearDown(self):
        self.clean()


try:
    mongo_backend = backends.MongoBackend()
except ImportError:
    print "Skipping mongo backend tests: you must pip install mongoengine."
except exceptions.MongodbConnectionError:
    print "Skipping mongo backend tests: unable to connect to mongodb."
else:
    class MongoBackendTestCase(unittest.TestCase, BaseBackendTest):            
        def setUp(self):
            self.backend = mongo_backend

        def tearDown(self):
            self.clean()
            self.backend.db.drop_collection('bookmark')


        def test_filter_bookmarks(self):
            pass

        def test_bookmark_model(self):
            pass


# REGISTRY TESTS

class RegistryTestCase(unittest.TestCase, BookmarkTestMixin):
    def setUp(self):
        self.library = handlers.Registry()

    def _get_handler(self):
        class CustomHandler(handlers.Handler):
            pass
        return CustomHandler

    def test_registry(self):
        instance = self.create_instance('handlers')
        model = type(instance)

        self.library.register(model)

        handler = self.library.get_handler(model)
        self.assertTrue(isinstance(handler, handlers.Handler))
        
        self.assertRaises(exceptions.AlreadyHandled, self.library.register,
            model)
        
        self.library.unregister(type(instance))
        self.assertRaises(exceptions.NotHandled, self.library.unregister,
            model)

        self.assertEqual(self.library.get_handler(User), None)
        
        custom_handler = self._get_handler()
        key = 'custom'
        self.library.register([User, model], custom_handler, default_key=key)

        handler = self.library.get_handler(self.create_user('handlers'))
        self.assertTrue(isinstance(handler, custom_handler))
        self.assertEqual(handler.default_key, key)


# FORM TESTS

class FormTestCase(unittest.TestCase, BookmarkTestMixin):
    def setUp(self):
        self.backend = backends.ModelBackend()
        self.form_class = forms.BookmarkForm
        user, instance, self.key = self.get_user_instance_key('form1')
        self.bookmark = self.backend.add(user, instance, self.key)
        self.instance = self.create_instance('form2')
        self.request = self.get_request(user)

    def tearDown(self):
        self.clean()

    def _get_initial(self, instance, key):
        return {
            'model':str(instance._meta),
            'object_id': str(instance.pk),
            'key': key,
        }

    def test_is_valid(self):
        # valid
        initial = self._get_initial(self.bookmark.content_object, self.key)
        form = self.form_class(self.request, self.backend, data=initial)
        self.assertTrue(form.is_valid())
        self.assertDictEqual(initial, form.cleaned_data)

        # invalid: user is not authenticated
        form = self.form_class(self.get_request(), self.backend, data=initial)
        self.assertFalse(form.is_valid())

        # invalid: instance not found
        initial['object_id'] = 0
        form = self.form_class(self.request, self.backend, data=initial)
        self.assertFalse(form.is_valid())

    def test_instance(self):
        initial =  self._get_initial(self.instance, self.key)
        form = self.form_class(self.request, self.backend, data=initial)
        self.assertEqual(self.instance, form.instance())

    def test_existance(self):
        initial = self._get_initial(self.bookmark.content_object, self.key)
        form = self.form_class(self.request, self.backend, data=initial)
        self.assertTrue(form.bookmark_exists())
        
        initial =  self._get_initial(self.instance, self.key)
        form = self.form_class(self.request, self.backend, data=initial)
        self.assertFalse(form.bookmark_exists())

    def test_add(self):
        initial = self._get_initial(self.instance, self.key)
        form = self.form_class(self.request, self.backend, data=initial)
        form.is_valid()
        bookmark = form.save()
        self.assertIsInstance(bookmark, self.backend.get_model())
        self.assertIsNotNone(bookmark.pk)

    def test_remove(self):
        initial = self._get_initial(self.bookmark.content_object, self.key)
        form = self.form_class(self.request, self.backend, data=initial)
        form.is_valid()
        bookmark = form.save()
        self.assertIsInstance(bookmark, self.backend.get_model())
        self.assertIsNone(bookmark.pk)

    def test_invalid_call(self):
        initial = self._get_initial(self.instance, self.key)
        form = self.form_class(self.get_request(), self.backend, data=initial)
        form.is_valid()
        self.assertRaises(ValueError, form.bookmark_exists)        


# TEMPLATETAGS TESTS

class TemplatetagsTestCase(unittest.TestCase, BookmarkTestMixin):
    def setUp(self):
        handlers.library.register(BookmarkTestModel)
        self.backend = backends.ModelBackend()
        user, instance, key = self.get_user_instance_key('templatetags1')
        self.bookmark1 = self.backend.add(user, instance, key)
        instance = self.create_instance('templatetags2')
        self.bookmark2 = self.backend.add(user, instance, settings.DEFAULT_KEY)
        self.instance = self.create_instance('templatetags3')
        self.request_anonymous = self.get_request()
        self.request = self.get_request(self.bookmark1.user)
        self.handler = handlers.library.get_handler(BookmarkTestModel)

    def tearDown(self):
        self.clean()
        handlers.library.unregister(BookmarkTestModel)

    def render(self, template, context_dict, request=None):
        context = Context(context_dict.copy())
        if request is not None:
            context['request'] = request
        html =  Template(template).render(context)
        return html.strip(), context

    def test_bookmark(self):
        # successfully retreiving a bookmark
        template = u"""
            {% load bookmarks_tags %}
            {% bookmark for instance using mykey as mybookmark %}
        """
        context_dict = {
            'instance': self.bookmark1.content_object,
            'mykey': self.bookmark1.key
        }
        html, context = self.render(template, context_dict, self.request)
        self.assertFalse(html)
        self.assertEqual(context['mybookmark'], self.bookmark1)
        # successfully retreiving a bookmark using hardcoded key,
        # dotted notation and default key
        template2 = u"""
            {% load bookmarks_tags %}
            {% bookmark for instances.0 as mybookmark %}
        """ 
        context_dict = {
            'instances': [self.bookmark2.content_object],
        }
        html, context = self.render(template2, context_dict, self.request)
        self.assertEqual(context['mybookmark'], self.bookmark2)
        # retreiving failure because of unexistent bookmark
        context_dict = {
            'instance': self.instance,
            'mykey': self.bookmark1.key
        }
        html, context = self.render(template, context_dict, self.request)
        self.assertIsNone(context.get('mybookmark'))
        # retreiving failure because of anonymous user
        context_dict = {
            'instance': self.bookmark1.content_object,
            'mykey': self.bookmark1.key
        }
        html, context = self.render(template, context_dict, 
            self.request_anonymous)
        self.assertIsNone(context.get('mybookmark'))
        # retreiving failure because the instance is not bookmarkable
        handlers.library.unregister(BookmarkTestModel)
        context_dict = {
            'instance': self.bookmark1.content_object,
            'mykey': self.bookmark1.key
        }
        html, context = self.render(template, context_dict, self.request)
        self.assertIsNone(context.get('mybookmark'))
        handlers.library.register(BookmarkTestModel)


    def test_bookmark_form(self):
        # successfully retreiving a form for existent bokmark
        template = u"""
            {% load bookmarks_tags %}
            {% bookmark_form for instance using mykey as myform %}
        """
        context_dict = {
            'instance': self.bookmark2.content_object,
            'mykey': settings.DEFAULT_KEY,
        }
        html, context = self.render(template, context_dict, self.request)
        self.assertFalse(html)
        form = context['myform']
        form.is_valid()
        self.assertIsInstance(form, self.handler.form_class)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.bookmark_exists())
        self.assertEqual(form.instance(), self.bookmark2.content_object)
        # successfully retreiving a form for unexistent bokmark without key
        template2 = u"""
            {% load bookmarks_tags %}
            {% bookmark_form for instance as myform %}
        """
        context_dict = {
            'instance': self.instance,
        }
        html, context = self.render(template2, context_dict, self.request)
        self.assertFalse(html)
        form = context['myform']
        form.is_valid()
        self.assertIsInstance(form, self.handler.form_class)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.bookmark_exists())
        self.assertEqual(form.instance(), self.instance)
        # retreiving failure because the key is not allowed
        context_dict = {
            'instance': self.bookmark1.content_object,
            'mykey': self.bookmark1.key,
        }
        html, context = self.render(template, context_dict, self.request)
        self.assertFalse(html)
        self.assertIsNone(context.get('myform'))
        # successfully retreiving a form with dotted notation and different key
        template3 = u"""
            {% load bookmarks_tags %}
            {% bookmark_form for instances.0 using mykey as myform %}
        """
        context_dict = {
            'instances': [self.bookmark1.content_object],
            'mykey': self.bookmark1.key,
        }
        backup = self.handler.allowed_keys
        self.handler.allowed_keys = [self.bookmark1.key]
        html, context = self.render(template3, context_dict, self.request)
        self.assertFalse(html)
        form = context['myform']
        form.is_valid()
        self.assertIsInstance(form, self.handler.form_class)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.bookmark_exists())
        self.assertEqual(form.instance(), self.bookmark1.content_object)
        self.handler.allowed_keys = backup
        # retreiving failure because of anonymous user
        context_dict = {
            'instance': self.bookmark2.content_object,
            'mykey': settings.DEFAULT_KEY,
        }
        html, context = self.render(template, context_dict, 
            self.request_anonymous)
        self.assertFalse(html)
        self.assertIsNone(context.get('myform'))
        # retreiving failure because the instance is not bookmarkable
        handlers.library.unregister(BookmarkTestModel)
        html, context = self.render(template, context_dict, self.request)
        self.assertIsNone(context.get('myform'))
        handlers.library.register(BookmarkTestModel)
        # return html
        template4 = u"""
            {% load bookmarks_tags %}
            {% bookmark_form for instance %}
        """
        context_dict = {
            'instance': self.instance,
        }
        html, context = self.render(template4, context_dict, self.request)
        self.assertTrue(html)

    def test_ajax_bookmark_form(self):
        template = u"""
            {% load bookmarks_tags %}
            {% ajax_bookmark_form for instance %}
        """
        context_dict = {
            'instance': self.instance,
        }
        html, context = self.render(template, context_dict, self.request)
        self.assertTrue(html)

    def test_bookmarks(self):
        self.clean()
        user1 = self.create_user('templatetags_bookmark_1')
        user2 = self.create_user('templatetags_bookmark_2')
        instance1 = self.create_instance('templatetags_bookmark_1')
        instance2 = self.create_instance('templatetags_bookmark_2')
        key1, key2 = 'templatetags_bookmark_1', 'templatetags_bookmark_2'
        bookmark1 = self.backend.add(user1, instance1, key1)
        bookmark2 = self.backend.add(user1, instance1, key2)
        bookmark3 = self.backend.add(user2, instance1, key1)
        bookmark4 = self.backend.add(user2, instance2, key2)
        bookmark5 = self.backend.add(user1, user2, key1)
        # getting all bookmarks
        template = u"""
            {% load bookmarks_tags %}
            {% bookmarks as bookmarks %}
        """
        context_dict = {}
        html, context = self.render(template, context_dict, self.request)
        bookmarks = list(context['bookmarks'])
        expected = [bookmark1, bookmark2, bookmark3, bookmark4, bookmark5]
        self.assertEqual(bookmarks, expected)
        # getting all bookmarks of instance1
        template = u"""
            {% load bookmarks_tags %}
            {% bookmarks of instance as bookmarks %}
        """
        context_dict = {
            'instance': instance1,
        }
        html, context = self.render(template, context_dict, self.request)
        bookmarks = list(context['bookmarks'])
        expected = [bookmark1, bookmark2, bookmark3]
        self.assertEqual(bookmarks, expected)
        # getting all bookmarks of user2
        template = u"""
            {% load bookmarks_tags %}
            {% bookmarks by user as bookmarks %}
        """
        context_dict = {
            'user': user2,
        }
        html, context = self.render(template, context_dict, self.request)
        bookmarks = list(context['bookmarks'])
        expected = [bookmark3, bookmark4]
        self.assertEqual(bookmarks, expected)
        # getting all bookmarks of dotted user1 reversed
        template = u"""
            {% load bookmarks_tags %}
            {% bookmarks by users.0 reversed as bookmarks %}
        """
        context_dict = {
            'users': [user1],
        }
        html, context = self.render(template, context_dict, self.request)
        bookmarks = list(context['bookmarks'])
        expected = [bookmark5, bookmark2, bookmark1]
        self.assertEqual(bookmarks, expected)
        # getting all bookmarks of key2
        template = u"""
            {% load bookmarks_tags %}
            {% bookmarks using key as bookmarks %}
        """
        context_dict = {
            'key': key2,
        }
        html, context = self.render(template, context_dict, self.request)
        bookmarks = list(context['bookmarks'])
        expected = [bookmark2, bookmark4]
        self.assertEqual(bookmarks, expected)
        # getting all bookmarks of instance1 model name and key1
        template = u"""
            {% load bookmarks_tags %}
            {% bookmarks of 'bookmarks.bookmarktestmodel' using mykey as bookmarks %}
        """
        context_dict = {
            'mykey': key1,
        }
        html, context = self.render(template, context_dict, self.request)
        bookmarks = list(context['bookmarks'])
        expected = [bookmark1, bookmark3]
        self.assertEqual(bookmarks, expected)
        # getting all bookmarks of user1 model name
        template = u"""
            {% load bookmarks_tags %}
            {% bookmarks of 'auth.user' as mybookmarks %}
        """
        context_dict = {}
        html, context = self.render(template, context_dict, self.request)
        bookmarks = list(context['mybookmarks'])
        expected = [bookmark5]
        self.assertEqual(bookmarks, expected)
        # getting all bookmarks of user2, instance1 and key1
        template = u"""
            {% load bookmarks_tags %}
            {% bookmarks of instances.0 by myuser using key as bookmarks %}
        """
        context_dict = {
            'instances': [instance1],
            'myuser': user2,
            'key': key1,
        }
        html, context = self.render(template, context_dict, self.request)
        bookmarks = list(context['bookmarks'])
        expected = [bookmark3]
        self.assertEqual(bookmarks, expected)
        # getting all bookmarks with user2 and hardcoded key1 reversed
        template = u"""
            {% load bookmarks_tags %}
            {% bookmarks by user using 'templatetags_bookmark_1' reversed as bookmarks %}
        """
        context_dict = {
            'user': user2,
        }
        html, context = self.render(template, context_dict, self.request)
        bookmarks = list(context['bookmarks'])
        expected = [bookmark3]
        self.assertEqual(bookmarks, expected)
        # getting all bookmarks with unexistent key
        template = u"""
            {% load bookmarks_tags %}
            {% bookmarks using 'wrong_key' as bookmarks %}
        """
        context_dict = {}
        html, context = self.render(template, context_dict, self.request)
        self.assertFalse(context['bookmarks'])


# VIEWS TESTS

class BookmarkViewTestCase(unittest.TestCase, BookmarkTestMixin):
    def setUp(self):
        handlers.library.register(BookmarkTestModel)
        self.handler = handlers.library.get_handler(BookmarkTestModel)
        self.backend = self.handler.backend

    def tearDown(self):
        self.clean()
        handlers.library.unregister(BookmarkTestModel)

    def get_data(self, instance, key=None):
        return {
            'model':str(instance._meta),
            'object_id': str(instance.pk),
            'key': key or self.handler.default_key,
        }

    def get_post_request(self, user=None, post_data=None, url='/', **kwargs):
        return RequestFactory(user, **kwargs).post(url, post_data or {})

    def test_success(self):
        user = self.create_user('view_bookmark_success')
        instance = self.create_instance('view_bookmark_success')
        http_referer = '/bookmark/success/'
        request = self.get_post_request(user, self.get_data(instance), 
            HTTP_REFERER=http_referer)
        # adding bookmark
        response = views.bookmark(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], http_referer)
        exists = self.backend.exists(user, instance, self.handler.default_key)
        self.assertTrue(exists)
        # removing bookmark
        response = views.bookmark(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], http_referer)
        exists = self.backend.exists(user, instance, self.handler.default_key)
        self.assertFalse(exists)

    def test_fail_invalid_method(self):
        user = self.create_user('view_bookmark_success')
        request = self.get_request(user)
        response = views.bookmark(request)
        self.assertEqual(response.status_code, 403)
    
    def test_fail_invalid_model(self):
        user = self.create_user('view_bookmark_success')
        instance = self.create_instance('view_bookmark_success')
        data = self.get_data(instance)
        data['model'] = 'invalid.model'
        request = self.get_post_request(user, data)
        response = views.bookmark(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, views.ERRORS['model'])

    def test_fail_invalid_instance(self):
        user = self.create_user('view_bookmark_success')
        instance = self.create_instance('view_bookmark_success')
        data = self.get_data(instance)
        data['object_id'] = str(int(data['object_id']) + 1)
        request = self.get_post_request(user, data)
        response = views.bookmark(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, self.handler.failure_message)

    def test_fail_invalid_key(self):
        user = self.create_user('view_bookmark_success')
        instance = self.create_instance('view_bookmark_success')
        data = self.get_data(instance)
        data['key'] = 'invalid_key'
        request = self.get_post_request(user, data)
        response = views.bookmark(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, views.ERRORS['key'])

    def test_fail_not_handled(self):
        user = self.create_user('view_bookmark_success')
        instance = self.create_instance('view_bookmark_success')
        handlers.library.unregister(BookmarkTestModel)
        request = self.get_post_request(user, self.get_data(instance))
        response = views.bookmark(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, views.ERRORS['handler'])
        handlers.library.register(BookmarkTestModel)

    def test_fail_not_authenticated(self):
        instance = self.create_instance('view_bookmark_success')
        request = self.get_post_request(None, self.get_data(instance))
        response = views.bookmark(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, self.handler.failure_message)


try:
    from bookmarks.views.generic import BookmarksForView, BookmarksByView
except ImportError:
    print "Skipping class based views tests: unsupported by current Django version."
else:

    class ClassBasedViewTextMixin(BookmarkTestMixin):
        def get_view(self, **kwargs):
            return self.view_class.as_view(**kwargs)

        def create_bookmarks(self):
            self.user1 = self.create_user('class_based_test1')
            self.user2 = self.create_user('class_based_test2')
            self.instance1 = self.create_instance('class_based_test1')
            self.instance2 = self.create_instance('class_based_test2')
            self.instance3 = self.create_instance('class_based_test3')
            self.key1 = 'class_based_test1'
            self.key2 = 'class_based_test2'
            self.bookmark1 = self.backend.add(self.user1, self.instance1, self.key1)
            self.bookmark2 = self.backend.add(self.user1, self.instance2, self.key1)
            self.bookmark3 = self.backend.add(self.user1, self.instance1, self.key2)
            self.bookmark4 = self.backend.add(self.user1, self.instance3, self.key2)
            self.bookmark5 = self.backend.add(self.user2, self.instance1, self.key1)

        def get_data_from_response(self, response):
            return (
                response.context_data['object'], 
                list(response.context_data['bookmarks'])
            )


    class BookmarksForViewTestCase(unittest.TestCase, ClassBasedViewTextMixin):
        view_class = BookmarksForView

        def setUp(self):
            self.backend = backends.ModelBackend()

        def tearDown(self):
            self.clean()

        def test_normal(self):
            self.create_bookmarks()
            view = self.get_view(model=BookmarkTestModel)
            request = self.get_request()
            response = view(request, pk=self.instance1.id)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.template_name, 
                ['bookmarks/bookmarktestmodel_bookmarks.html'])

            instance, bookmarks = self.get_data_from_response(response)
            self.assertEqual(instance, self.instance1)
            expected = [self.bookmark5, self.bookmark3, self.bookmark1]
            self.assertEqual(bookmarks, expected)

        def test_queryset_template_not_reversed(self):
            self.create_bookmarks()
            queryset = BookmarkTestModel.objects.exclude(pk=self.instance2.pk)
            view = self.get_view(queryset=queryset, template_name='test.html',
                reversed_order=False)
            request = self.get_request()
            response = view(request, pk=self.instance1.id)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.template_name, 
                ['test.html', 'bookmarks/bookmarktestmodel_bookmarks.html'])

            instance, bookmarks = self.get_data_from_response(response)
            self.assertEqual(instance, self.instance1)
            expected = [self.bookmark1, self.bookmark3, self.bookmark5]
            self.assertEqual(bookmarks, expected)

        def test_key(self):
            self.create_bookmarks()
            view = self.get_view(model=BookmarkTestModel, key=self.key2)
            request = self.get_request()
            response = view(request, pk=self.instance1.id)
            self.assertEqual(response.status_code, 200)

            instance, bookmarks = self.get_data_from_response(response)
            self.assertEqual(instance, self.instance1)
            expected = [self.bookmark3]
            self.assertEqual(bookmarks, expected)

        def test_empty(self):
            self.create_bookmarks()
            view = self.get_view(model=BookmarkTestModel, key=self.key2)
            request = self.get_request()
            response = view(request, pk=self.instance2.id)
            self.assertEqual(response.status_code, 200)

            instance, bookmarks = self.get_data_from_response(response)
            self.assertEqual(instance, self.instance2)
            self.assertFalse(bookmarks)


    class BookmarksByViewTestCase(unittest.TestCase, ClassBasedViewTextMixin):
        view_class = BookmarksByView

        def setUp(self):
            self.backend = backends.ModelBackend()

        def tearDown(self):
            self.clean()

        def test_normal(self):
            self.create_bookmarks()
            view = self.get_view()
            request = self.get_request()
            response = view(request, pk=self.user1.id)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.template_name, 
                ['auth/user_bookmarks.html'])

            instance, bookmarks = self.get_data_from_response(response)
            self.assertEqual(instance, self.user1)
            expected = [self.bookmark4, self.bookmark3, self.bookmark2, self.bookmark1]
            self.assertEqual(bookmarks, expected)

        def test_queryset_template_not_reversed(self):
            self.create_bookmarks()
            queryset = User.objects.exclude(pk=self.user2.pk)
            view = self.get_view(queryset=queryset, template_name='test.html',
                reversed_order=False)
            request = self.get_request()
            response = view(request, pk=self.user1.id)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.template_name, 
                ['test.html', 'auth/user_bookmarks.html'])

            instance, bookmarks = self.get_data_from_response(response)
            self.assertEqual(instance, self.user1)
            expected = [self.bookmark1, self.bookmark2, self.bookmark3, self.bookmark4]
            self.assertEqual(bookmarks, expected)

        def test_key(self):
            self.create_bookmarks()
            view = self.get_view(model=User, key=self.key1)
            request = self.get_request()
            response = view(request, pk=self.user1.id)
            self.assertEqual(response.status_code, 200)

            instance, bookmarks = self.get_data_from_response(response)
            self.assertEqual(instance, self.user1)
            expected = [self.bookmark2, self.bookmark1]
            self.assertEqual(bookmarks, expected)

        def test_empty(self):
            self.create_bookmarks()
            view = self.get_view(key=self.key2)
            request = self.get_request()
            response = view(request, pk=self.user2.id)
            self.assertEqual(response.status_code, 200)

            instance, bookmarks = self.get_data_from_response(response)
            self.assertEqual(instance, self.user2)
            self.assertFalse(bookmarks)


# MODEL TESTS

class ModelsTestCase(unittest.TestCase, BookmarkTestMixin):
    def setUp(self):
        self.backend = backends.ModelBackend()
        self.user1 = self.create_user('models_test1')
        self.user2 = self.create_user('models_test2')
        self.instance1 = self.create_instance('models_test1')
        self.instance2 = self.create_instance('models_test2')
        self.instance3 = self.create_instance('models_test3')
        self.instance4 = self.create_instance('models_test4')
        self.key1 = 'models_test1'
        self.key2 = 'models_test2'
        self.backend.add(self.user1, self.instance2, self.key1)
        self.backend.add(self.user1, self.instance4, self.key1)
        self.backend.add(self.user1, self.instance2, self.key2)
        self.backend.add(self.user1, self.instance3, self.key2)

    def tearDown(self):
        self.clean()

    def annotate(self, *args, **kwargs):
        return list(annotate_bookmarks(*args, **kwargs))

    def assertAttrIndexTrue(self, objects, indexes, attr_name='is_bookmarked'):
        for num, i in enumerate(objects):
            attr = getattr(i, attr_name)
            if num in indexes:
                self.assertTrue(attr)
            else:
                self.assertFalse(attr)

    def test_key1(self):
        objects = self.annotate(BookmarkTestModel, self.key1, self.user1)
        self.assertAttrIndexTrue(objects, [1, 3])

    def test_key2_queryset(self):
        objects = self.annotate(BookmarkTestModel.objects.all(), self.key2, 
            self.user1)
        self.assertAttrIndexTrue(objects, [1, 2])

    def test_key1_attr(self):
        objects = self.annotate(BookmarkTestModel, self.key1, self.user1,
            attr='test_attr')
        self.assertAttrIndexTrue(objects, [1, 3], attr_name='test_attr')

    def test_key2_user2(self):
        objects = self.annotate(BookmarkTestModel, self.key2, self.user2)
        self.assertAttrIndexTrue(objects, [])
