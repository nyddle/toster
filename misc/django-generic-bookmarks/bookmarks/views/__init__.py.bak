from django.db.models import get_model
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import http

from bookmarks import handlers, signals, utils
from bookmarks.templatetags import bookmarks_tags

ERRORS = {
    'model': u'Invalid model.',
    'handler': u'Unregistered model.',
    'key': u'Invalid key.',
    'instance': u'Invalid instance.',
}

def bookmark(request):
    """
    Add or remove a bookmark based on POST data.
    """
    if request.method == 'POST':
        
        # getting handler
        model_name = request.POST.get('model', u'')
        model = get_model(*model_name.split('.'))
        if model is None:
            # invalid model -> bad request
            return http.HttpResponseBadRequest(ERRORS['model'])
        handler = handlers.library.get_handler(model)
        if handler is None:
            # bad or unregistered model -> bad request
            return http.HttpResponseBadRequest(ERRORS['handler'])

        # getting form
        form = handler.get_form(request, data=request.POST)
        if form.is_valid():
            instance = form.instance()
            bookmark_model = handler.backend.get_model()

            # validating the bookmark key
            key = handler.get_key(request, instance, form.cleaned_data['key'])
            if not handler.allow_key(request, instance, key):
                return http.HttpResponseBadRequest(ERRORS['key'])
                                
            # pre-save signal: receivers can stop the bookmark process
            # note: one receiver is always called: *handler.pre_save*
            # handler can disallow the vote
            responses = signals.bookmark_pre_save.send(sender=bookmark_model, 
                form=form, request=request)
    
            # if one of the receivers returns False then bookmark process 
            # must be killed
            for receiver, response in responses:
                if response == False:
                    return http.HttpResponseBadRequest(
                        u'Receiver %r killed the bookmark process' % 
                        receiver.__name__)
            
            # adding or removing the bookmark
            bookmark = handler.save(request, form)
            created = bool(bookmark.pk)
        
            # post-save signal
            # note: one receiver is always called: *handler.post_save*
            signals.bookmark_post_save.send(sender=bookmark_model, 
                bookmark=bookmark, request=request, created=created)
    
            # process completed successfully: redirect
            return handler.response(request, bookmark, created)
        
        # form is not valid: must handle errors
        return handler.fail(request, form.errors)
        
    # only answer POST requests
    return http.HttpResponseForbidden('Forbidden.')


def ajax_form(request, extra_context=None, 
    template=bookmarks_tags.BookmarkFormNode.template_name):
    """
    Called by *ajax_bookmark_form* templatetag, this view accepts AJAX
    requests and returns the bookmark form html fragment.

    The template used to render the context is the same as the one
    used by *bookmark_form* templatetag.
    """
    if request.is_ajax():
        # getting handler
        model_name = request.GET.get('model', u'')
        model = get_model(*model_name.split('.'))
        if model is None:
            # invalid model -> bad request
            return http.HttpResponseBadRequest(ERRORS['model'])
        handler = handlers.library.get_handler(model)
        if handler is None:
            # bad or unregistered model -> bad request
            return http.HttpResponseBadRequest(ERRORS['handler'])

        # getting instance
        object_id = request.GET.get('object_id')
        try:
            instance = model.objects.get(pk=object_id)
        except (TypeError, ValueError, model.DoesNotExist):
            # invalid instance -> bad request
            return http.HttpResponseBadRequest(ERRORS['instance'])

        # getting form
        form = handler.get_form(request, data=request.GET)

        # validating the bookmark key
        key = handler.get_key(request, instance, request.GET.get('key'))
        if not handler.allow_key(request, instance, key):
            return http.HttpResponseBadRequest(ERRORS['key'])

        # context and template
        context = bookmarks_tags.BookmarkFormNode.get_template_context(
            request, form, instance, key)
        context['next_url'] = request.META.get('HTTP_REFERER') or '/'
        if extra_context is not None:
            context.update(extra_context)
        template = utils.get_templates(instance, key, template)

        # output
        return render_to_response(template, context, 
            context_instance=RequestContext(request))

        
    # only answer AJAX requests
    return http.HttpResponseForbidden('Forbidden.')
