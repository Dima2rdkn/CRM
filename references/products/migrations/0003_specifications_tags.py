# Generated by Django 4.0.4 on 2022-04-30 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_categories_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='specifications',
            name='tags',
            field=models.TextField(blank=True, verbose_name='Тэги'),
        ),
    ]
