# Generated by Django 3.1.7 on 2022-07-17 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210326_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='link_img_produto',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produto',
            name='link_produto',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
    ]
