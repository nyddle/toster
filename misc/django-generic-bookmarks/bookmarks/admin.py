from django.contrib import admin

from bookmarks import models

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'key', 'user', 'created_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    search_fields = ('user', 'key')
    readonly_fields = ('user',)

admin.site.register(models.Bookmark, BookmarkAdmin)
