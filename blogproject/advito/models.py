from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone


def user_directory_path(instance, filename):
    return f'user_{instance.author.id}/posts/{filename}'

def user_avatar_path(instance, filename):
	return f'user_{instance.user.id}/avatar/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile') 
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    about = models.TextField(verbose_name="Информация о пользователе", blank=True, max_length=300)
    phone = models.CharField(verbose_name="Телефон", null=True, blank=True, max_length=50)
    avatar = models.ImageField(verbose_name="Фото пользователя", upload_to=user_avatar_path)
    town = models.CharField(verbose_name="Город", null=True, blank=True, max_length=30)
    subscribers = models.ManyToManyField(User, blank=True, verbose_name="Подписчики пользователя", related_name='subscribers') 
    reviews = models.ManyToManyField(User, blank=True, verbose_name="Отзывы о пользователе", related_name='reviews') 
    messages = models.ManyToManyField(User, blank=True, verbose_name="Сообщения пользователю", related_name='messages') 

    def __str__(self):
        return f'Profile for user - {self.user}'


class CategoryPost(models.Model):
    """Категория объявления"""
    name_category = models.CharField(verbose_name="Категория", max_length=100)

    def __str__(self):
        return f'Category - {self.name_category}'


class Post(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryPost, on_delete=models.CASCADE, verbose_name="Категория")
    price = models.IntegerField(verbose_name="Цена")
    name_descript = models.CharField(max_length=200,  blank=True, verbose_name="Название объявления")
    description = models.TextField(max_length=1000, blank=True, verbose_name="Описание объявления")
    image = models.ImageField(upload_to=user_directory_path, verbose_name="Фото объявления")
    date_pub = models.DateTimeField(default=timezone.now, verbose_name="Дата объявления")
    date_adit = models.DateTimeField(default=timezone.now, verbose_name="Дата редактирования")
    
    def __str__(self):
        return f'Post - {self.name_descript}; {self.category}; Autor - {self.author}'


class HistoryPost(models.Model):
    """ История объявления"""
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post, blank=True, related_name='post')
    date_create = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    def __str__(self):
        return f'Post - {self.date_create}; date_create - {self.date_create}'


class FavoritePost(models.Model):
    """Избранное объявление"""
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name="Объявление", on_delete=models.CASCADE)
    

class Comment(models.Model):
    """Отзыв об объявлении"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700)
    in_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Autor - {self.author}; Date_publish - {self.date_publish}'
