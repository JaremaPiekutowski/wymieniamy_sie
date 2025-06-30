from django.contrib import admin

from .models import Book, BookGenre


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_added', 'user')
    list_filter = ('date_added', 'user')
    ordering = ('-date_added',)
    search_fields = ('title', 'author')
    list_select_related = ('user', 'genre')
    list_per_page = 20

    # Optionally, if you have a lot of users, you can use a raw_id_fields for user
    raw_id_fields = ('user',)


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(BookGenre)
