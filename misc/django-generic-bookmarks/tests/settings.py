DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
DATABASE_ENGINE = 'sqlite3'
ROOT_URLCONF = ''
SITE_ID = 1
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'bookmarks',
)
GENERIC_BOOKMARKS_MONGODB = {"NAME": "test_generic_bookmarks"}
ROOT_URLCONF = 'urls'