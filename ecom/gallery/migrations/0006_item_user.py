# Generated by Django 3.0.8 on 2020-08-13 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_auto_20200809_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.CharField(default='Deleted User', max_length=30),
        ),
    ]
