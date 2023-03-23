##################################################################################
#
#   Модели для работы с ТОВАРАМИ И УСЛУГАМИ
#   (С)2022 Дворядкин Дмитрий aka dima2rdkn
###################################################################################

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from references.suppliers.models import Supplier
from references.measure.models import Measure
from references.stores.models import Stores


########################################
# Категории товаров и услуг
# Иерархическая структура по полю parent


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

########################################
# Товары и услуги
#


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

    def get_query_set(self):
        return super(Products, self).get_query_set().exclude(isActive=False)

    @staticmethod
    def get_list(**kwargs):
        product_list = Products.objects.filter(isActive=True).order_by('title')
        if ('category' in kwargs) and (kwargs['category']):
            product_list = product_list.filter(category=kwargs['category'])
        return product_list

    @staticmethod
    def get_list_image(**kwargs):
        product_list = Products.get_list(**kwargs)
        for prod in product_list:
            img = ProductImages.objects.filter(product=prod, primary=True).first()
            prod.image = img.image
        return product_list

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def image(self):
        # очень странная функция. Стырена на просторах тырнета.
        # Пользоваться, конечно можно, но осторожно :)
        img = ProductImages.objects.filter(product=self, primary=True)
        if img is not None:
            image = img.image.url
        else:
            image = ""
        return image


def image_folder(instance, filename):
    return "images/products/{0}/{1}".format(instance.product.slug, filename)

########################################
# Галерея изображений товара
# Подчинение модели Product по полю product


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

########################################
# Спецификация товара
# Подчинение модели Product по полю product


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

########################################
# Отзывы о товаре
# Подчинение модели Product по полю product


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

########################################
# Комплектация товара
# Товар может быть составным (букеты, композиции, подарочные наборы)
# Подчинение модели Product по полю product
# Логика включает две модели базовую (Composition) и табличную (CompositionTable)


class Composition(models.Model):
    product = models.ForeignKey(Products, related_name='product_cmp', verbose_name='Товар', on_delete=models.CASCADE)
    createdBy = models.ForeignKey(User, related_name='composition_author', on_delete=models.PROTECT,
                                  verbose_name='Автор')
    createdOn = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return "состав для " + self.product

    class Meta:
        verbose_name = 'Комплект'
        verbose_name_plural = 'Комплекты'


class CompositionTable(models.Model):
    docptr = models.ForeignKey(Composition, verbose_name='Комплект', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='product_cmp_tbl', verbose_name='Товар', on_delete=models.PROTECT)
    qntty = models.FloatField(verbose_name='Количество')

    def __str__(self):
        return self.docptr + "( " + self.product + ")"

    class Meta:
        verbose_name = 'Комплект ТЧ'
        verbose_name_plural = 'Комплекты ТЧ'
