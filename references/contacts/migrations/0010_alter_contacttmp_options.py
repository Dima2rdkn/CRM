# Generated by Django 4.0.4 on 2022-08-26 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0009_contacttmp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contacttmp',
            options={'ordering': ['first_name']},
        ),
    ]