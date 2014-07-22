from django.utils.functional import memoize
from django.contrib.contenttypes.models import ContentType

_get_content_type_for_model_cache = {}

def get_content_type_for_model(model):
    return ContentType.objects.get_for_model(model)

get_content_type_for_model = memoize(get_content_type_for_model, 
    _get_content_type_for_model_cache, 1)

def get_templates(instance, key, name, base='bookmarks'):
    """
    Return a list of template names based on given *instance* and
    bookmark *key*.

    For example, if *name* is 'form.html'::

        bookmarks/[app_name]/[model_name]/[key]/form.html
        bookmarks/[app_name]/[model_name]/form.html
        bookmarks/[app_name]/[key]/form.html
        bookmarks/[app_name]/form.html
        bookmarks/[key]/form.html
        bookmarks/form.html
    """
    app_label = instance._meta.app_label
    module_name = instance._meta.module_name
    return [
        '%s/%s/%s/%s/%s' % (base, app_label, module_name, key, name),
        '%s/%s/%s/%s' % (base, app_label, module_name, name),
        '%s/%s/%s/%s' % (base, app_label, key, name),
        '%s/%s/%s' % (base, app_label, name),
        '%s/%s/%s' % (base, key, name),
        '%s/%s' % (base, name),
    ]
