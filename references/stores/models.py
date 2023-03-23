from django.db import models
from django.urls import reverse


class Stores(models.Model):
    name = models.CharField(max_length=128, verbose_name='Наименование')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_list(**kwargs):
        return Stores.objects.all().order_by('name')

    def get_absolute_url(self):
        return reverse('store_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'
