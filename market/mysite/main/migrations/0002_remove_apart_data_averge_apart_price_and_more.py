# Generated by Django 4.1.7 on 2023-10-19 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apart_data',
            name='averge_apart_price',
        ),
        migrations.AddField(
            model_name='apart_data',
            name='averge_apart_price1',
            field=models.BigIntegerField(default=0),
        ),
    ]
