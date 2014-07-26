"""
Django settings for toster project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import dj_database_url
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '879pcns$i75*g!lqt!p0kfo__)+1e7jn_)9ni2d(ix4_+z+%56'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

AUTH_USER_MODEL = 'core.MyUser'

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'debug_toolbar',
    'taggit',
    'south',
    'secretballot',
    'likes',
    'rest_framework',
    'haystack',
    'toster',
    'core',
    'bookmarks'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "likes.middleware.SecretBallotUserIpUseragentMiddleware",
)

ROOT_URLCONF = 'toster.urls'

WSGI_APPLICATION = 'toster.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# Parse database configuration from $DATABASE_URL
DATABASES = {'default': dj_database_url.config(default='postgres://localhost/toster') }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

FIXTURE_DIRS = (
   '../fixtures/',
)

#    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
REST_FRAMEWORK = {
    'PAGINATE_BY': 10
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
# STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "social_auth.context_processors.social_auth_by_type_backends"
)



# social auth
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    # 'social_auth.backends.facebook.FacebookBackend',
    # 'social_auth.backends.google.GoogleOAuthBackend',
    # 'social_auth.backends.google.GoogleOAuth2Backend',
    # 'social_auth.backends.google.GoogleBackend',
    # 'social_auth.backends.yahoo.YahooBackend',
    # 'social_auth.backends.browserid.BrowserIDBackend',
    # 'social_auth.backends.contrib.linkedin.LinkedinBackend',
    # 'social_auth.backends.contrib.disqus.DisqusBackend',
    # 'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    # 'social_auth.backends.contrib.orkut.OrkutBackend',
    # 'social_auth.backends.contrib.foursquare.FoursquareBackend',
    # 'social_auth.backends.contrib.github.GithubBackend',
    # 'social_auth.backends.contrib.vk.VKOAuth2Backend',
    # 'social_auth.backends.contrib.live.LiveBackend',
    # 'social_auth.backends.contrib.skyrock.SkyrockBackend',
    # 'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    # 'social_auth.backends.contrib.readability.ReadabilityBackend',
    # 'social_auth.backends.contrib.fedora.FedoraBackend',
    # 'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# have no idea what is it
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16

TWITTER_CONSUMER_KEY = 'RBvaJN9JXmSWQqwRnHa8DQigD'
TWITTER_CONSUMER_SECRET = 'sr6R4ib1r2wVhxPWFCn4zC2I9jvyLFCOxwKnS8gHEX91QldjjW'

SOCIAL_AUTH_TWITTER_KEY = 'RBvaJN9JXmSWQqwRnHa8DQigD'
SOCIAL_AUTH_TWITTER_SECRET = 'sr6R4ib1r2wVhxPWFCn4zC2I9jvyLFCOxwKnS8gHEX91QldjjW'

SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter', )

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/members/'
LOGIN_ERROR_URL = '/login-error/'

try:
    from .local_settings import *
except:
    pass
