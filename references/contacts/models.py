from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class ContactGroup(models.Model):
    title = models.CharField(max_length=64, unique=True, db_index=True,
                             verbose_name='Наименование')
    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.SET_NULL,
                               verbose_name='Группа')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа клиентов'
        verbose_name_plural = 'Группы клиентов'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('contacts_list_by_group', args=[self.id])


class Contact(models.Model):
    MESSENGERS = [
        ('SM', 'SMS'),
        ('WA', 'WhatsApp'),
        ('VB', 'Viber'),
        ('TG', 'Telegram'),
        ('VK', 'VKontakte'),
        ('FB', 'Facebook'),
        ('WC', 'WeChat'),
        ('SC', 'Snapchat'),
        ('SK', 'Skype'),
    ]
    category = models.ForeignKey(ContactGroup, on_delete=models.PROTECT,
                                 db_index=True, null=True, verbose_name='Группа')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    phone2 = models.CharField(max_length=20, verbose_name='Телефон2')
    messenger = models.CharField(max_length=2, choices=MESSENGERS, default='SM'
                                 , verbose_name='Мессенджер')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(blank=True, upload_to='images/contacts/',
                              verbose_name='Изображение')
    createdBy = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE,
                                  verbose_name='Автор')
    createdOn = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def get_absolute_url(self):
        return reverse('contact_detail', args=[self.id])
