from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Categories(models.Model):
    name = models.CharField(max_length=128, verbose_name='Категория')
    slug = models.SlugField(unique=True)
    image = models.ImageField(blank=True, upload_to='images/products/categories/',
                              verbose_name='Изображение')
    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.SET_NULL,
                               verbose_name='Группа')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Products(models.Model):
    category = models.ForeignKey(Categories, verbose_name='Категория', on_delete=models.PROTECT)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    article = models.CharField(blank=True, max_length=16, verbose_name='Артикул')
    description = models.TextField(blank=True, verbose_name='Описание')
    createdBy = models.ForeignKey(User, related_name='manager', on_delete=models.PROTECT,
                                  verbose_name='Автор')
    createdOn = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


def image_folder(instance, filename):
    return "images/products/{0}/{1}".format(instance.product.slug, filename)


class ProductImages(models.Model):
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=image_folder,
                              verbose_name='Изображение')
    primary = models.BooleanField(default=False,)

    def __str__(self):
        return '[image]'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Specifications(models.Model):
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.CASCADE)
    composition = models.TextField(blank=True, verbose_name='Состав')
    height = models.IntegerField(default=0, verbose_name='Высота')
    width = models.IntegerField(default=0, verbose_name='Ширина')
    size = models.IntegerField(default=0, verbose_name='Размер')
    tags = models.TextField(blank=True, verbose_name='Тэги')

    def __str__(self):
        return 'ТТХ'

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class Feedback(models.Model):
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.CASCADE)
    author = models.CharField(max_length=64, verbose_name='Автор')
    message = models.TextField(blank=True, verbose_name='Сообщение')
    rating = models.IntegerField(default=0, verbose_name='Оценка')

    def __str__(self):
        return self.rating

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
