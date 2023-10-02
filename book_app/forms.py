from django import forms
from .models import CommentUser, BookCommentUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CommentUserForm(forms.ModelForm):

    class Meta:
        model = CommentUser
        fields = ['name', 'email', 'comment', 'phone']

        labels = {
            'name': 'Имя пользователя',
            'email': 'Почта',
            'comment': 'Комментарий',
            'phone': 'Телефон'

        }
        errors_message = {
            'email': {
                'required': 'Поле не должно быть пустым',
            },
            'comment': {
                'required': 'Поле не должно быть пустым'
            }
        }


class BookCommentUserForm(forms.ModelForm):

    class Meta:

        model = BookCommentUser
        fields = ['comment_user']

        labels = {
            'name_user': 'Имя пользователя',
            'comment_user': 'Комментарий к книге'
        }

        errors_message = {
            'mame': {
                'required': 'Поле не должно быть пустым'
            },

        }


class RegistrationForm(UserCreationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторение пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='Почта', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:

        model = User
        fields = ['username', 'password1', 'password2', 'email']


class AuthorizationForm(AuthenticationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ProfileSearchForm(forms.Form):
    name = forms.CharField(label='Поле поиска', required=False)