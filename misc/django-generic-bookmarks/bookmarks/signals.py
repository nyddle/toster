from django.dispatch import Signal

# fired before a bookmark is added or removed
bookmark_pre_save = Signal(providing_args=['form', 'request'])
# fired after a bookmark is added or removed
bookmark_post_save = Signal(providing_args=['bookmark', 'request', 'created'])
