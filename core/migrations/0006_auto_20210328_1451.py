# Generated by Django 3.1.7 on 2022-07-17 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_compareproduto_comparado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compareproduto',
            name='comparado',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Houve comparação?'),
        ),
    ]
