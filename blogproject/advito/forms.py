from django import forms
from django.contrib.auth.models import User 
from .models import Post, Profile, FavoritePost, Comment, Message


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['category', 'price', 'name_descript','description', 'image']

        labels = {
            'category':'Выберите категорию',
            'price': 'Укажите цену',
            'name_descript':'Заголовок поста',
            'description': 'Описание поста',
            'image':'Выберите файл',
        }

        widjets = {
            'category':forms.Textarea(attrs={
                'class': 'form__category', 
                'placeholder': 'Описание поста',
            }),
            'price':forms.Textarea(attrs={
                'class': 'form__textarea', 
                'placeholder': 'Цена',
            }),
            'name_descript':forms.Textarea(attrs={
                'class': 'form__title', 
                'placeholder': 'Название поста',
            }),
            'description':forms.Textarea(attrs={
                'class': 'form__text', 
                'placeholder': 'Описание поста',
            }),
            'image':forms.ClearableFileInput(attrs={
                'class': 'form__file', 
                'type': 'file',
            }),
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        
        fields = ['birth_date', 'about', 'phone', 'avatar', 'town']
        
        labels = {
            'birth_date': 'День рождения',
            'about': 'О себе', 
            'phone': 'Телефон', 
            'avatar': 'Аватар', 
            'town': 'Город', 
        }

        widjets = {
            'birth_date': forms.Textarea(),

            'about': forms.Textarea(attrs={
                'class': 'form__', 
                'placeholder': 'Описание поста',
            }),
            'phone': forms.Textarea(), 
            
            'town': forms.Textarea(), 
            
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form__file', 
                'type': 'file',
            }),
        }

class PersonalForm(forms.ModelForm):
    
    class Meta:
        model = User

        fields = ['username', 'first_name', 'last_name', 'password', 'email']

        labels = {
            'username': 'Новый псевдоним',
            'first_name': 'Новое Имя', 
            'last_name': 'Новая Фамилия', 
            'password': 'Новый Пароль', 
            'email': 'Новая Почта',
        }

        widjets = {
            'username': forms.CharField(initial='Your name'),
            'first_name': forms.CharField(),
            'last_name': forms.CharField(), 
            'password': forms.PasswordInput(), 
            'email': forms.EmailField(),
        } 

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment

        fields =['text']

        labels = {
            'text': 'Оставьте комментарий'
        }

        widjets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст комментария'
            })
        } 

class MessageForm(forms.ModelForm):
    
    class Meta:
        model = Message

        fields =['text']

        labels = {
            'text': 'Текст комментария',
        }

        widjets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст комментария'
            }),
        } 

