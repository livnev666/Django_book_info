from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout, login
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book, Author, Categories, CommentUser, BookCommentUser
from .forms import CommentUserForm, RegistrationForm, AuthorizationForm, ProfileSearchForm, BookCommentUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import F, Sum, Max, Min, Count, Avg
import json
# Create your views here.

# with open(r'D:\My_Dgango_Project_PC\book_info\book_app\data.json') as file:
#     data = json.load(file)
#
#
# for i in data:
#     new_category = Categories(
#         categories=i.get('categories'),
#         isbn=i.get('isbn')
#
#     )
#     new_category.save()

# for i in data:
#     new_author = Author(
#         authors=i.get('authors'),
#         isbn=i.get('isbn')
#     )
#     new_author.save()


# for item in data:
#     book = Book(
#         # title=item['title'],
#         # isbn=item.get('isbn'),
#         # pageCount=item.get('pageCount'),
#         # thumbnailUrl=item.get('thumbnailUrl'),
#         # shortDescription=item.get('shortDescription'),
#         # longDescription=item.get('longDescription'),
#         publishedDate=item.get('publishedDate')
#     )
#     book.save()


dc_bar = [

    {'title': 'Категории', 'url_name': 'categories'},
    {'title': 'Книги', 'url_name': 'book-list'},
    {'title': 'Авторы', 'url_name': 'authors-list'},
    {'title': 'Обратная связь', 'url_name': 'comment_user'}

]


class RegisterView(CreateView):

    form_class = RegistrationForm
    template_name = 'book_app/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['dc_bar'] = dc_bar
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('book-list')


class AuthorizationView(LoginView):

    form_class = AuthorizationForm
    template_name = 'book_app/authorization.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        context['dc_bar'] = dc_bar
        return context

    def get_success_url(self):
        return reverse('categories')


def log_out_user(request):

    logout(request)
    return redirect('log_in')


class AllCategoriesId(ListView):

    model = Book
    template_name = 'book_app/categories_id.html'
    context_object_name = 'book_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'cat_cat_id': Categories.objects.get(id=self.kwargs['cat_id']),
            'dc_bar': dc_bar,

        })
        return context


class AllCategories(ListView):

    model = Categories
    form_class = ProfileSearchForm
    template_name = 'book_app/list_categories.html'
    context_object_name = 'cat'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'book': Book,
            'title': 'Категории',
            # 'cat': Categories.objects.all().values('categories').distinct(),
            'count_cat': Categories.objects.all().aggregate(Count('categories')),
            'dc_bar': dc_bar,
        })
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Categories.objects.filter(categories__icontains=form.cleaned_data['name'])
        return Categories.objects.all()


class AllBook(ListView):

    model = Book
    form_class = ProfileSearchForm
    template_name = 'book_app/list_book.html'
    context_object_name = 'book'
    paginate_by = 30

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'new_cat': Categories,
            'count_book': Book.objects.all().aggregate(Count('title')),
            'title': 'Книги',
            'dc_bar': dc_bar,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_qs = queryset.filter(Q(is_published=True))
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Book.objects.filter(title__icontains=form.cleaned_data['name'])
        return filter_qs, Book.objects.all()


class AllAuthors(ListView):

    model = Author
    form_class = ProfileSearchForm
    template_name = 'book_app/list_authors.html'
    context_object_name = 'authors'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'new_book': Book,
            'title': 'Авторы книг',
            'dc_bar': dc_bar,
        })
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Author.objects.filter(authors__icontains=form.cleaned_data['name'])
        return Author.objects.all()


class DetailBook(FormMixin, DetailView):

    model = Book
    form_class = BookCommentUserForm
    template_name = 'book_app/about_book.html'
    context_object_name = 'one_book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dc_bar': dc_bar,
            'one_book': get_object_or_404(Book, pk=self.kwargs['pk'])
        })
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('one_book', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.name_book = self.get_object()
        self.object.name_user = self.request.user
        self.object.save()
        return super().form_valid(form)


class AddCommentUser(LoginRequiredMixin, CreateView):

    model = CommentUser
    form_class = CommentUserForm
    template_name = 'book_app/contact.html'
    success_url = '/book'
    login_url = 'log_in'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оставить сообщение'
        context['dc_bar'] = dc_bar
        return context







