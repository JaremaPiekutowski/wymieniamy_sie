from django.contrib import admin

from .models import Book, BookGenre


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_added', 'user')
    list_filter = ('date_added', 'user')
    ordering = ('date_added',)
    search_fields = ('title', 'author')


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(BookGenre)
