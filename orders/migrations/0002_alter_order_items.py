# Generated by Django 5.1.5 on 2025-01-15 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.TextField(verbose_name='Список блюд'),
        ),
    ]
