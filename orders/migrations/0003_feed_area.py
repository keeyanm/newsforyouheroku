# Generated by Django 2.1.5 on 2020-06-05 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200602_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='area',
            field=models.CharField(default='None', max_length=64),
        ),
    ]
