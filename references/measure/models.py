from django.db import models
from django.urls import reverse


class Measure(models.Model):
    name = models.CharField(max_length=8, verbose_name='сокр.')
    description = models.CharField(max_length=128, verbose_name='Описание')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('measure_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
