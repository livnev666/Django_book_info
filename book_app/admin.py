from django.contrib import admin, messages
from .models import Book, Author, Categories, CommentUser, BookCommentUser
from django.db.models import QuerySet
from django.utils.safestring import mark_safe

# Register your models here.


@admin.register(BookCommentUser)
class BookCommentUserAdmin(admin.ModelAdmin):

    list_display = ['id', 'name_user', 'comment_user']
    list_display_links = ['name_user']
    list_per_page = 5
    search_fields = ['name_user']


@admin.register(CommentUser)
class CommentUserAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'email', 'comment', 'phone']
    list_display_links = ['name']
    list_per_page = 5
    search_fields = ['email']


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):

    list_display = ['id', 'categories', 'isbn']
    list_display_links = ['categories']
    list_per_page = 20
    search_fields = ['categories']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ['id', 'authors', 'isbn']
    list_display_links = ['authors']
    list_per_page = 10


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'isbn', 'image_photo_book', 'shortDescription', 'longDescription', 'is_published']
    list_editable = ['is_published']
    list_display_links = ['title']
    list_per_page = 8
    ordering = ['id', 'title']
    filter_horizontal = ['authors', 'categories']
    search_fields = ['title', 'id']

    def image_photo_book(self, obj):
        if obj.thumbnailUrl:
            return mark_safe("<img src='{}' width='80'/>".format(obj.thumbnailUrl.url))
    image_photo_book.__name__ = 'Фото'