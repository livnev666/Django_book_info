from django.urls import path
from book_app import views as views_book_app

urlpatterns = [

    path('', views_book_app.AllCategories.as_view(), name='categories'),
    path('book/', views_book_app.AllBook.as_view(), name='book-list'),
    path('book/<int:pk>/', views_book_app.DetailBook.as_view(), name='one_book'),
    path('authors/', views_book_app.AllAuthors.as_view(), name='authors-list'),
    path('categories/<int:cat_id>/', views_book_app.AllCategoriesId.as_view(), name='cat-id'),
    path('comment/', views_book_app.AddCommentUser.as_view(), name='comment_user'),
    path('registration/', views_book_app.RegisterView.as_view(), name='register'),
    path('login/', views_book_app.AuthorizationView.as_view(), name='log_in'),
    path('logout/', views_book_app.log_out_user, name='log_out'),

]