# Generated by Django 4.2.4 on 2023-09-02 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Aktywny'),
        ),
    ]