from django.conf import settings

from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import AbstractBaseUser, UserManager as DjangoMyUserManager, PermissionsMixin

# this one is for likes
import secretballot
# and this onу for bookmarks
from bookmarks.handlers import library


class MyUserManager(DjangoMyUserManager):
    def _create_user(self, name, email, password,
                     is_staff, is_superuser, **extra_fields):
        if not name:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, is_staff=is_staff,
                          is_active=True, is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email=None, password=None, **extra_fields):
        return self._create_user(name, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, name, email, password, **extra_fields):
        return self._create_user(name, email, password, True, True,
                                 **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(blank=True, null=True)
    reg_date = models.DateTimeField('date registered', auto_now_add=True)
    rating = models.IntegerField(default=0)
    about = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email']

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name



class Question(models.Model):
    question = models.CharField(max_length=200)
    details = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    views = models.IntegerField(default=0)
    answered = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    section = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    tags = TaggableManager()


secretballot.enable_voting_on(Question)
library.register(Question)
library.register(MyUser)



