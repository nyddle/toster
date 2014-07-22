import re

from django import template
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django import http
from django.db.models import get_model

from bookmarks import handlers, utils, exceptions

register = template.Library()

def _parse_args(parser, token, expression):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        error = u"%r tag requires arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError, error
    # args validation
    match = expression.match(arg)
    if not match:
        error = u"%r tag has invalid arguments" % tag_name
        raise template.TemplateSyntaxError, error
    return match.groupdict()
 

class BaseNode(template.Node):
    def __init__(self, instance, key, varname):
        # instance
        self.instance = template.Variable(instance)
        # key
        self.key_variable = None
        if key is None:
            self.key = None
        elif key[0] in ('"', "'") and key[-1] == key[0]:
            self.key = key[1:-1]
        else:
            self.key_variable = template.Variable(key)
        # varname
        self.varname = varname

    def _get_key(self, context):
        if self.key_variable:
            return self.key_variable.resolve(context)
        return self.key


BOOKMARK_EXPRESSION = re.compile(r"""
    ^ # begin of line
    for\s+(?P<instance>[\w.]+) # instance
    (\s+using\s+(?P<key>[\w.'"]+))? # key
    \s+as\s+(?P<varname>\w+) # varname
    $ # end of line
""", re.VERBOSE)

@register.tag
def bookmark(parser, token):
    """
    Return as a template variable a bookmark object for the given instance
    and key, and for current user.

    Usage:
    
    .. code-block:: html+django

        {% bookmark for *instance* [using *key*] as *varname* %}
    
    The key can be given hardcoded (surrounded by quotes) 
    or as a template variable.
    Note that if the key is not given, it will be generated using 
    the handler's *get_key* method, that, if not overridden, returns
    the default key. 

    The template variable will be None if:
        - the user is not authenticated
        - the instance is not bookmarkable
        - the bookmark does not exist
    """
    return BookmarkNode(**_parse_args(parser, token, BOOKMARK_EXPRESSION))

class BookmarkNode(BaseNode):   
    def render(self, context):
        # user validation
        request = context['request']
        if request.user.is_anonymous():
            return u''

        # instance and handler
        instance = self.instance.resolve(context)
        handler = handlers.library.get_handler(instance)
        # handler validation
        if handler is None:
            return u''
        
        # key
        key = handler.get_key(request, instance, self._get_key(context))

        # retreiving bookmark
        try:
            context[self.varname] = handler.get(request.user, instance, key)
        except exceptions.DoesNotExist:
            pass
        return u''


BOOKMARK_FORM_EXPRESSION = re.compile(r"""
    ^ # begin of line
    for\s+(?P<instance>[\w.]+) # instance
    (\s+using\s+(?P<key>[\w.'"]+))? # key
    (\s+as\s+(?P<varname>\w+))? # varname
    $ # end of line
""", re.VERBOSE)

@register.tag
def bookmark_form(parser, token):
    """
    Return, as html or as a template variable, a Django form to add or remove 
    a bookmark for the given instance and key, and for current user.

    Usage:
    
    .. code-block:: html+django

        {% bookmark_form for *instance* [using *key*] [as *varname*] %}
    
    The key can be given hardcoded (surrounded by quotes) 
    or as a template variable.
    Note that if the key is not given, it will be generated using 
    the handler's *get_key* method, that, if not overridden, returns
    the default key. 

    If the *varname* is used then it will be a context variable 
    containing the form.
    Otherwise the form is rendered using the first template found in the order
    that follows::

        bookmarks/[app_name]/[model_name]/[key]/form.html
        bookmarks/[app_name]/[model_name]/form.html
        bookmarks/[app_name]/[key]/form.html
        bookmarks/[app_name]/form.html
        bookmarks/[key]/form.html
        bookmarks/form.html
    
    The *app_name* and *model_name* refer to the instance given as
    argument to this templatetag.

    Example:

    .. code-block:: html+django

        {% bookmark_form for myinstance using 'mykey' as form %}

        {% if form %}
            {% if user.is_authenticated %}
                <form action="{% url bookmarks_bookmark %}" method="post" accept-charset="UTF-8" class="bookmarks_form">
                    {% csrf_token %}
                    {{ form }}
                    {% with form.bookmark_exists as exists %}
                        {# another hidden input is created to handle javascript submit event #}
                        <input class="bookmarks_toggle" type="submit" value="add"{% if exists %} style="display: none;"{% endif %}/>
                        <input class="bookmarks_toggle" type="submit" value="remove"{% if not exists %} style="display: none;"{% endif %}/>
                    {% endwith %}                
                    <span class="error" style="display: none;">Error during process</span>
                </form>
            {% else %}
                <a href="{{ login_url }}?{{ next }}={{ request.get_full_path }}">add</a>
            {% endif %}
        {% endif %}


    The template variable (or the html) will be None if:
        - the user is not authenticated
        - the instance is not bookmarkable
        - the key is not allowed

    AJAX is also supported using jQuery, e.g.:

    .. code-block:: html+django

        {% load bookmarks_tags %}

        <script src="path/to/jquery.js" type="text/javascript"></script>
        <script src="{{ STATIC_URL }}bookmarks/bookmarks.js" type="text/javascript"></script>

        {% bookmark_form for article %}
    """
    return BookmarkFormNode(**_parse_args(parser, token, 
        BOOKMARK_FORM_EXPRESSION))

class BookmarkFormNode(BaseNode):

    template_name = 'form.html'

    @classmethod
    def get_template_context(cls, request, form, instance, key):
        """
        Return the template context: used only when the *as variable* 
        argument is not used in templatetag invocation.
        """
        return {
            'form': form,
            'instance': instance,
            'key': key,
            'login_url': settings.LOGIN_URL,
            'next': REDIRECT_FIELD_NAME,
        }

    def render(self, context):
        # user validation
        request = context['request']
        if request.user.is_anonymous() and self.varname is not None:
            return u''

        # instance and handler
        instance = self.instance.resolve(context)
        handler = handlers.library.get_handler(instance)
        # handler validation
        if handler is None:
            return u''
        
        # key validation
        key = handler.get_key(request, instance, self._get_key(context))
        if not handler.allow_key(request, instance, key):
            return u''

        # creating form
        data = {
            'model': str(instance._meta),
            'object_id': str(instance.pk),
            'key': key,
        }
        form = handler.get_form(request, data=data)

        if self.varname is None:
            # rendering the form
            ctx = template.RequestContext(request, 
                self.get_template_context(context, form, instance, key))
            templates = utils.get_templates(instance, key, self.template_name)
            return template.loader.render_to_string(templates, ctx)
        else:
            # form as template variable
            context[self.varname] = form
            return u''


AJAX_BOOKMARK_FORM_EXPRESSION = re.compile(r"""
    ^ # begin of line
    for\s+(?P<instance>[\w.]+) # instance
    (\s+using\s+(?P<key>[\w.'"]+))? # key
    $ # end of line
""", re.VERBOSE)

@register.tag
def ajax_bookmark_form(parser, token):
    """
    Use this just like the *bookmark_form* templatetag.
    The only difference here is that it always render a form template
    (so you can't use the *as varname* part), and the form template
    is rendered using an AJAX request.

    This is useful for example when you want to show add/remove
    bookamrk interaction for authenticated users even in a cached template.

    You need to load jQuery before using this templatetag.
    """
    return AJAXBookmarkFormNode(varname=None, **_parse_args(parser, token, 
        AJAX_BOOKMARK_FORM_EXPRESSION))

class AJAXBookmarkFormNode(BookmarkFormNode):
    template_name = 'ajax_form.html'

    @classmethod
    def get_template_context(cls, request, form, instance, key):
        ctx = super(AJAXBookmarkFormNode, cls).get_template_context(
            request, form, instance, key)
        template = u'bookmarkform_%(key)s-%(model)s-%(object_id)s'
        url = reverse('bookmarks_ajax_form')
        querydict = http.QueryDict('', mutable=True)
        querydict.update(form.data)
        ctx.update({
            'form_id': template % form.data,
            'url': u'%s?%s' % (url, querydict.urlencode()),
        })
        return ctx


BOOKMARKS_EXPRESSION = re.compile(r"""
    ^ # begin of line
    (of\s+(?P<model>[\w.'"]+))? # model
    (\s*by\s+(?P<user>[\w.]+))? # user
    (\s*using\s+(?P<key>[\w.'"]+))? # key
    (\s*(?P<order>reversed))? # order
    \s*as\s+(?P<varname>\w+) # varname
    $ # end of line
""", re.VERBOSE)

@register.tag
def bookmarks(parser, token):
    """
    Return as a template variable all bookmarks, with possibility to filter 
    them by user, or to take only bookmarks of a particular model and
    using a specified key. It is also possible to reverse the order 
    of bookmarks (by default they are ordered by date).

    Usage:
    
    .. code-block:: html+django

        {% bookmarks [of *model*] [by *user*] [using *key*] [reversed] as *varname* %}

    Examples:

    .. code-block:: html+django

        {# get all bookmarks saved by myuser #}
        {% bookmarks by myuser as myuser_bookmarks %}

        {# get all bookmarks for myinstance using mykey #}
        {% bookmarks of myinstance using *mykey* as bookmarks %}

        {# getting all bookmarks for model 'myapp.mymodel' in reverse order #}
        {% bookmarks of 'myapp.mymodel' reversed as varname %}

    Note that the args *model* can be:

        - a model name as string (e.g.: 'myapp.mymodel')
        - a model instance

    The key can be given hardcoded (surrounded by quotes) 
    or as a template variable.
    """
    return BookmarksNode(**_parse_args(parser, token, BOOKMARKS_EXPRESSION))

class BookmarksNode(template.Node):
    def __init__(self, model, user, key, order, varname):
        # model
        self.model_variable = None
        if model is None:
            self.model = None
        elif model[0] in ('"', "'") and model[-1] == model[0]:
            self.model = model[1:-1]
        else:
            self.model_variable = template.Variable(model)
        # user
        self.user = template.Variable(user) if user else None
        # key
        self.key_variable = None
        if key is None:
            self.key = None
        elif key[0] in ('"', "'") and key[-1] == key[0]:
            self.key = key[1:-1]
        else:
            self.key_variable = template.Variable(key)
        # order
        self.reverse_order = bool(order)
        # varname
        self.varname = varname

    def render(self, context):
        # parsing arguments to build lookups
        lookups = {'reversed': self.reverse_order}
        # model
        if self.model_variable:
            lookups['instance'] = self.model_variable.resolve(context)
        elif self.model is not None:
            lookups['model'] = get_model(*self.model.split('.'))
        # user
        if self.user is not None:
            lookups['user'] = self.user.resolve(context)
        # key
        if self.key_variable:
            lookups['key'] = self.key_variable.resolve(context)
        elif self.key is not None:
            lookups['key'] = self.key
        # retreiving bookmarks
        context[self.varname] = handlers.library.backend.filter(**lookups)
        return u''
