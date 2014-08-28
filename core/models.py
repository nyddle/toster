from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.conf import settings

from django.db import models
from taggit.managers import TaggableManager
from taggit.models import Tag
from django.contrib.auth.models import AbstractBaseUser, UserManager as DjangoMyUserManager, PermissionsMixin

# this one is for likes
import secretballot
# and this only for bookmarks
from bookmarks.handlers import library
# this is for activity stream
from actstream import registry, action

from .utils import *


class MyUserManager(DjangoMyUserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff,
                          is_active=True, is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True, null=True)
    reg_date = models.DateTimeField('date registered', auto_now_add=True)
    rating = models.IntegerField(default=0)
    about = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to=avatar_file_name, default='avatar/default.png')

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username


class UserProfile(models.Model):
    """
    User profile. Storage for additional information about user.
    """
    user = models.OneToOneField(MyUser)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    about = models.TextField(blank=True)
    user_avatar = models.ImageField(upload_to='avatar/', default='avatar/default.png')

    def __str__(self):
        return 'Profile of user: %s' % self.user.username


class Question(models.Model):
    question = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default="")
    details = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    views = models.IntegerField(default=0)
    answered = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    section = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        super(Question, self).save(*args, **kwargs)
        action.send(self.author, verb='asked a question')
        for tag in self.tags.all():
            action.send(tag, verb='new question')


secretballot.enable_voting_on(Question)
library.register(Question)
library.register(MyUser)

#TODO: this will change in 1.7: https://django-activity-stream.readthedocs.org/en/latest/configuration.html
registry.register(MyUser)
registry.register(Question)
registry.register(Tag)

