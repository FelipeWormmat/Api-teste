# Generated by Django 3.1.7 on 2022-07-17 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210326_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='tp_promocao',
        ),
        migrations.AddField(
            model_name='produto',
            name='promocao',
            field=models.BooleanField(default=False, verbose_name='Possui Promoção?'),
        ),
    ]
