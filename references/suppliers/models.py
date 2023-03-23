from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class SupplierGroup(models.Model):
    title = models.CharField(max_length=64, unique=True, db_index=True,
                             verbose_name='Наименование')
    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.SET_NULL,
                               verbose_name='Группа')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа поставщиков'
        verbose_name_plural = 'Группы поставщиков'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('suppliers_list_by_group', args=[self.id])


class Supplier(models.Model):

    category = models.ForeignKey(SupplierGroup, on_delete=models.SET_NULL,
                                 db_index=True, null=True, verbose_name='Группа')
    name = models.CharField(max_length=125, verbose_name='Наименование')
    full_name = models.CharField(max_length=255, verbose_name='Полное наименование')
    email = models.EmailField(blank=True, verbose_name='Почта')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    phone2 = models.CharField(blank=True, max_length=20, verbose_name='Телефон2')
    address = models.TextField(blank=True, verbose_name='Адрес')
    post_address = models.TextField(blank=True, verbose_name='Почтовый адрес')
    INN = models.CharField(max_length=12, verbose_name='ИНН')
    KPP = models.CharField(max_length=9, verbose_name='КПП')
    director = models.CharField(max_length=128, verbose_name='Руководитель')
    description = models.TextField(blank=True, verbose_name='Описание')
    createdBy = models.ForeignKey(User, related_name='supplier_author', on_delete=models.PROTECT,
                                  verbose_name='Автор')
    createdOn = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщик'

    @staticmethod
    def get_list(**kwargs):
        supplier_list = Supplier.objects.filter(isActive=True).order_by('name')
        if ('category' in kwargs) and (kwargs['category']):
            supplier_list = supplier_list.filter(category=kwargs['category'])
        return supplier_list

    def get_absolute_url(self):
        return reverse('supplier_detail', args=[self.id])


