# Generated by Django 4.2.4 on 2023-09-09 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_book_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Nazwisko i imię autora/ki'),
        ),
    ]
