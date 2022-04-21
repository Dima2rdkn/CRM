# Generated by Django 4.0 on 2022-04-19 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contacts', '0002_auto_20210818_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='createdBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='author', to='auth.user', verbose_name='Автор'),
        ),
    ]
