from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Categories(models.Model):

    categories = models.CharField(max_length=100, blank=True, null=True, verbose_name='Категория')
    isbn = models.CharField(max_length=100, blank=True, null=True, verbose_name='Порядковый номер')

    def __str__(self):
        return f'{self.categories} {self.isbn}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['categories']


class Author(models.Model):

    authors = models.CharField(max_length=100, blank=True, null=True, verbose_name='Авторы')
    isbn = models.CharField(max_length=100, blank=True, null=True, verbose_name='Порядковый номер')

    def __str__(self):
        return f'{self.authors}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['authors']


class Book(models.Model):

    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название книги')
    isbn = models.CharField(max_length=100, blank=True, null=True, verbose_name='Порядковый номер')
    pageCount = models.IntegerField(blank=True, null=True, verbose_name='Количество страниц книги')
    thumbnailUrl = models.ImageField(upload_to='gallary/%y/%m/%d', blank=True, null=True, default='', verbose_name='Фото')
    shortDescription = models.CharField(max_length=250, null=True, blank=True, verbose_name='Короткое описание книги')
    longDescription = models.TextField(blank=True, null=True, verbose_name='Полное описание книги')
    is_published = models.BooleanField(blank=True, null=True, default=True, verbose_name='Опубликовано')
    publishedDate = models.CharField(max_length=100, null=True, blank=True, verbose_name='Время создания')

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')

    authors = models.ManyToManyField(Author, blank=True, related_name='authors_book')
    categories = models.ManyToManyField(Categories, blank=True, related_name='categories_book')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title']


class CommentUser(models.Model):

    name = models.CharField(max_length=40, verbose_name='Имя пользователя')
    email = models.CharField(max_length=100, verbose_name='Почта')
    comment = models.TextField(verbose_name='Сообщение')
    phone = models.BigIntegerField(null=True, blank=True, verbose_name='Номер телефона')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'


class BookCommentUser(models.Model):
    name_user = models.CharField(max_length=50, verbose_name='Имя пользователя')
    comment_user = models.TextField(verbose_name='Комментарий')
    create_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    name_book = models.ForeignKey(Book, on_delete=models.CASCADE,
                                     null=True, blank=True, verbose_name='Книга', related_name='commentuser_book')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Комментарий к книге'
        verbose_name_plural = 'Комментарии к книгам'