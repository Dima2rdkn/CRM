# Generated by Django 4.0.4 on 2022-05-06 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_specifications_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='article',
            field=models.CharField(blank=True, max_length=16, verbose_name='Артикул'),
        ),
    ]
