from django.contrib import admin

from .models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bookmark, BookmarkAdmin)

