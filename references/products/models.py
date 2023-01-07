from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import get_object_or_404


class Categories(models.Model):
    name = models.CharField(max_length=128, verbose_name='Категория')
    slug = models.SlugField(unique=True, editable=True)
    image = models.ImageField(blank=True, upload_to='images/products/categories/',
                              verbose_name='Изображение')
    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.SET_NULL,
                               verbose_name='Группа')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Categories, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @staticmethod
    def get_list(**kwargs):
        if ('slug' in kwargs) and (kwargs['slug']):
            category_list = get_object_or_404(Categories, slug=kwargs['slug'])
        else:
            category_list = Categories.objects.all()
        return category_list

    def get_absolute_url(self):
        return reverse('products_list_by_cat',  kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Products(models.Model):
    category = models.ForeignKey(Categories, verbose_name='Категория', on_delete=models.PROTECT)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True, editable=True)
    article = models.CharField(blank=True, max_length=16, verbose_name='Артикул')
    description = models.TextField(blank=True, verbose_name='Описание')
    createdBy = models.ForeignKey(User, related_name='manager', on_delete=models.PROTECT,
                                  verbose_name='Автор')
    createdOn = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Products, self).save(*args, **kwargs)

    @staticmethod
    def get_list(**kwargs):
        product_list = Products.objects.filter(isActive=True).order_by('title')
        if ('category' in kwargs) and (kwargs['category']):
            product_list = product_list.filter(category=kwargs['category'])
        return product_list

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
        return self.product.title + ' [image]'

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
